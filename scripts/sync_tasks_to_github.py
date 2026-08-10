#!/usr/bin/env python3
"""Sync unchecked TASKS.md items into GitHub issues.

Usage:
  GITHUB_TOKEN=... python3 scripts/sync_tasks_to_github.py --repo owner/name

Optional:
  --project-id <project_v2_id>    Add created/found issues to a GitHub Project V2
  --dry-run                       Print intended actions without creating issues

This script is intentionally conservative:
- it only syncs unchecked checklist items (`- [ ] ...`)
- it skips items under `## Done`
- it avoids duplicates by checking a stable sync marker in issue bodies
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


TASK_LINE_RE = re.compile(r"^- \[ \] (.+?)\s*$")
SECTION_RE = re.compile(r"^## (.+?)\s*$")
SUBSECTION_RE = re.compile(r"^### (.+?)\s*$")


@dataclass
class TaskItem:
    title: str
    section: str
    subsection: str | None
    line_no: int

    @property
    def marker(self) -> str:
        subsection = self.subsection or "-"
        return f"TASK_SYNC::{self.section}::{subsection}::{self.title}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="GitHub repo in owner/name format")
    parser.add_argument("--tasks-file", default="TASKS.md")
    parser.add_argument("--project-id", help="GitHub Project V2 node id")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def infer_repo() -> str:
    try:
        remote = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"],
                text=True,
            )
            .strip()
        )
    except Exception as exc:
        raise SystemExit(f"Cannot infer repo from git remote: {exc}") from exc

    patterns = [
        re.compile(r"git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$"),
        re.compile(r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$"),
    ]
    for pattern in patterns:
        match = pattern.match(remote)
        if match:
            return f"{match.group('owner')}/{match.group('repo')}"
    raise SystemExit(f"Unsupported GitHub remote format: {remote}")


def parse_tasks(tasks_path: Path) -> list[TaskItem]:
    if not tasks_path.exists():
        raise SystemExit(f"Tasks file not found: {tasks_path}")

    items: list[TaskItem] = []
    section = ""
    subsection: str | None = None

    for idx, raw_line in enumerate(tasks_path.read_text().splitlines(), start=1):
        section_match = SECTION_RE.match(raw_line)
        if section_match:
            section = section_match.group(1).strip()
            subsection = None
            continue

        subsection_match = SUBSECTION_RE.match(raw_line)
        if subsection_match:
            subsection = subsection_match.group(1).strip()
            continue

        if section == "Done":
            continue

        task_match = TASK_LINE_RE.match(raw_line)
        if task_match:
            items.append(
                TaskItem(
                    title=task_match.group(1).strip(),
                    section=section or "Uncategorized",
                    subsection=subsection,
                    line_no=idx,
                )
            )
    return items


def github_request(
    method: str,
    url: str,
    token: str,
    payload: dict | None = None,
) -> dict | list:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "allstar-task-sync",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, headers=headers, method=method, data=data)
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API error {exc.code}: {detail}") from exc


def graphql_request(token: str, query: str, variables: dict) -> dict:
    payload = {"query": query, "variables": variables}
    response = github_request("POST", "https://api.github.com/graphql", token, payload)
    if "errors" in response:
        raise SystemExit(f"GitHub GraphQL error: {response['errors']}")
    return response["data"]


def fetch_existing_issues(repo: str, token: str) -> list[dict]:
    owner, name = repo.split("/", 1)
    query = urllib.parse.urlencode(
        {
            "state": "open",
            "per_page": "100",
            "labels": "task-sync",
        }
    )
    url = f"https://api.github.com/repos/{owner}/{name}/issues?{query}"
    data = github_request("GET", url, token)
    return [issue for issue in data if "pull_request" not in issue]


def find_existing_issue(task: TaskItem, issues: list[dict]) -> dict | None:
    for issue in issues:
        body = issue.get("body") or ""
        if task.marker in body:
            return issue
    return None


def build_issue_body(task: TaskItem, repo: str) -> str:
    lines = [
        "Auto-generated from `TASKS.md`.",
        "",
        f"- Repo: `{repo}`",
        f"- Section: `{task.section}`",
        f"- Subsection: `{task.subsection or '-'} `",
        f"- Source line: `{task.line_no}`",
        "",
        "## Goal",
        "",
        task.title,
        "",
        "## Sync Marker",
        "",
        f"`{task.marker}`",
    ]
    return "\n".join(lines)


def create_issue(repo: str, token: str, task: TaskItem) -> dict:
    owner, name = repo.split("/", 1)
    payload = {
        "title": task.title,
        "body": build_issue_body(task, repo),
        "labels": ["task", "backlog", "task-sync"],
    }
    url = f"https://api.github.com/repos/{owner}/{name}/issues"
    return github_request("POST", url, token, payload)


def add_issue_to_project(token: str, project_id: str, issue_node_id: str) -> None:
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """
    graphql_request(
        token,
        mutation,
        {"projectId": project_id, "contentId": issue_node_id},
    )


def main() -> int:
    args = parse_args()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise SystemExit("Missing GITHUB_TOKEN environment variable")

    repo = args.repo or infer_repo()
    tasks = parse_tasks(Path(args.tasks_file))
    existing_issues = fetch_existing_issues(repo, token)

    print(f"Repo: {repo}")
    print(f"Found {len(tasks)} unchecked tasks in {args.tasks_file}")

    created = 0
    skipped = 0

    for task in tasks:
        existing = find_existing_issue(task, existing_issues)
        if existing:
            print(f"SKIP existing issue #{existing['number']}: {task.title}")
            if args.project_id:
                print(f"Ensure project linkage for issue #{existing['number']}")
                if not args.dry_run:
                    add_issue_to_project(token, args.project_id, existing["node_id"])
            skipped += 1
            continue

        print(f"CREATE issue: {task.title}")
        if args.dry_run:
            created += 1
            continue

        issue = create_issue(repo, token, task)
        if args.project_id:
            add_issue_to_project(token, args.project_id, issue["node_id"])
        created += 1

    print(f"Created: {created}")
    print(f"Skipped: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

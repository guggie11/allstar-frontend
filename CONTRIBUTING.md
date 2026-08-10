# Contributing

Dokumen ini menjelaskan cara `Team Onyet` dan manusia berkolaborasi di GitHub untuk repo ini.

## Prinsip

- GitHub adalah source of truth tunggal.
- Semua perubahan masuk lewat Pull Request.
- `main` harus tetap stabil.
- Satu issue mewakili satu pekerjaan yang jelas.
- Satu PR idealnya menyelesaikan satu issue atau satu bagian kecil dari issue besar.

## Workflow

1. Buat issue atau product brief.
2. `onyet-lead` memecah pekerjaan menjadi task kecil.
3. Jika perlu, `onyet-architect` menulis keputusan teknis.
4. `onyet-frontend` atau agen lain mengerjakan perubahan di branch terpisah.
5. Buat Pull Request.
6. Jalankan validasi yang relevan.
7. `onyet-qa` dan `onyet-reviewer` memeriksa hasilnya.
8. Manusia memberi approval akhir.
9. Merge ke `main`.

## Branch Naming

Gunakan salah satu format berikut:

- `feature/<short-name>`
- `fix/<short-name>`
- `chore/<short-name>`
- `docs/<short-name>`

Contoh:
- `feature/admin-login`
- `fix/login-error-state`
- `docs/team-onyet-workflow`

## Issue Standard

Setiap issue minimal harus memiliki:
- goal
- scope
- out of scope
- acceptance criteria
- risiko atau dependensi

Jika issue besar, pecah menjadi task lebih kecil sebelum implementasi.

## Pull Request Standard

Setiap Pull Request harus memuat:
- link issue terkait
- ringkasan perubahan
- daftar file atau area yang terdampak
- langkah validasi
- risiko yang diketahui
- screenshot jika ada perubahan UI

PR tidak boleh digabung jika:
- scope tidak jelas
- belum ada validasi
- ada blocker dari reviewer
- ada perubahan sensitif tanpa approval manusia

## Validation

Minimal salah satu validasi harus dicatat:
- lint
- typecheck
- unit test
- integration test
- manual QA steps

Jika tool belum tersedia, catat dengan jujur apa yang belum bisa diverifikasi.

## Review Rules

`onyet-reviewer` fokus pada:
- bug
- regresi
- maintainability
- keamanan dasar
- kekurangan test

Review summary boleh singkat, tetapi blocker harus spesifik dan bisa ditindaklanjuti.

## Human Approval Gate

Approval manusia wajib untuk:
- merge ke `main`
- perubahan arsitektur besar
- auth atau permission sensitif
- konfigurasi environment penting
- deploy ke staging atau production

## Definition of Done

Sebuah perubahan dianggap selesai jika:
- issue atau task-nya jelas
- PR sudah dibuat
- validasi tercatat
- review selesai
- approval manusia diperoleh

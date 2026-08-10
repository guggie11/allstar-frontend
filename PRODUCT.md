# Product

## Nama

Allstar Inline Skate Club Platform Frontend

## Overview

Allstar adalah aplikasi web untuk operasional `1 club inline skate` yang menjembatani:
- public
- member
- orang tua
- coach
- admin

Repo `allstar-frontend` berfokus pada pengalaman pengguna untuk web app yang dipakai oleh role-role tersebut, terutama member-facing dan admin-facing flow yang berhubungan dengan registrasi, pembayaran, progress, dan monitoring.

## Problem

Operasional club inline skate sering tersebar di chat, spreadsheet, dan catatan manual. Dampaknya:
- data member sulit dikelola
- status pendaftaran tidak rapi
- pembayaran bulanan sulit dipantau
- progress latihan tidak terdokumentasi konsisten
- orang tua dan member sulit memantau perkembangan
- admin tidak punya dashboard operasional yang jelas

## Goal

Frontend harus:
- memudahkan public melakukan registrasi
- memungkinkan admin memverifikasi registrasi
- memungkinkan member dan orang tua melihat status pembayaran dan perkembangan latihan
- memungkinkan coach mengelola attendance dan progress member sesuai level
- menyediakan dashboard admin yang ringkas dan jelas

## Product Scope

Produk MVP ini dibangun untuk:
- `1 club`
- `1 member` terhubung ke `1 orang tua`
- `1 member` hanya memiliki `1 level aktif` pada satu waktu
- coach bekerja `per level`
- pembayaran bulanan ditentukan berdasarkan `level`
- pembayaran dicatat `manual` oleh admin

## User Roles

### Public
- melihat informasi dasar club
- mengisi registrasi
- memilih program atau level saat registrasi

### Member
- melihat profil
- melihat level aktif
- melihat attendance
- melihat progress latihan
- melihat status pembayaran

### Orang Tua
- melihat data anak
- melihat progress anak
- melihat attendance anak
- melihat status pembayaran anak

### Coach
- melihat member berdasarkan level yang dia pegang
- mencatat attendance
- mengisi checklist skill
- memperbarui progress kurikulum member

### Admin
- memverifikasi registrasi
- mengaktifkan akun
- mengelola member
- mengelola level
- mengelola pembayaran bulanan
- melihat dashboard operasional

## MVP Features

### Registrasi dan Verifikasi
- public mengisi data registrasi
- public memilih program atau level
- sistem membuat akun dengan status `pending`
- admin memverifikasi atau menolak registrasi
- akun aktif hanya setelah verifikasi admin

### Member Management
- admin melihat dan mengelola daftar member
- admin menetapkan level aktif member
- admin menghubungkan member ke satu orang tua
- member dan orang tua melihat profil yang relevan

### Pembayaran Bulanan
- admin mencatat tagihan bulanan per member
- nominal pembayaran ditentukan oleh level
- admin mencatat pembayaran manual
- member dan orang tua melihat status pembayaran dan riwayat dasar

Status pembayaran:
- `belum bayar`
- `sudah bayar`
- `outstanding`

Definisi kerja:
- `belum bayar`: tagihan bulan berjalan belum dibayar
- `sudah bayar`: tagihan lunas
- `outstanding`: ada tunggakan dari periode sebelumnya

### Progress dan Attendance
- coach mencatat attendance member
- coach mengisi checklist skill
- coach memperbarui progress kurikulum
- member dan orang tua melihat perkembangan latihan

### Dashboard Admin
Dashboard admin minimal menampilkan:
- jumlah member
- ringkasan pembayaran
- distribusi member per level

## Registration Data

Data wajib registrasi saat ini:
- nama
- alamat
- tanggal lahir
- nomor HP
- email

Catatan:
detail pemisahan field milik member dan orang tua masih perlu difinalkan pada tahap desain berikutnya.

## Level Structure

Struktur level awal:
- `Beginner`
  - `Canopus`
- `Intermediate`
  - `Canopus 1`
  - `Canopus 2`
- `Advance`

Asumsi saat ini:
- `Beginner`, `Intermediate`, `Advance` adalah level utama
- `Canopus`, `Canopus 1`, `Canopus 2` adalah tahap kurikulum atau sub-level

## Core User Flows

### Flow 1: Registrasi ke Member Aktif
1. Public mengisi registrasi.
2. Public memilih program atau level.
3. Sistem membuat akun `pending`.
4. Admin memverifikasi registrasi.
5. Jika disetujui, akun menjadi aktif.
6. Member dan orang tua dapat mengakses data yang relevan.

### Flow 2: Pembayaran Bulanan
1. Admin membuat atau mencatat tagihan bulanan berdasarkan level member.
2. Admin mencatat pembayaran manual.
3. Sistem memperbarui status pembayaran.
4. Member dan orang tua melihat status pembayaran.

### Flow 3: Sesi Latihan ke Progress Record
1. Coach melihat daftar member berdasarkan level.
2. Coach mencatat attendance.
3. Coach mengisi checklist skill dan progress kurikulum.
4. Member dan orang tua melihat hasil perkembangan.

## Business Rules

- Sistem hanya untuk `1 club`.
- Satu member hanya punya `1 orang tua` yang terhubung.
- Satu member hanya punya `1 level aktif`.
- Registrasi tidak langsung aktif, harus diverifikasi admin.
- Nominal pembayaran bergantung pada level.
- Pembayaran dicatat manual, tanpa payment gateway di MVP.
- Coach bekerja berdasarkan level.
- Progress member harus berbasis kurikulum dan checklist skill.

## Non-Goals for MVP

MVP belum mencakup:
- multi-club support
- payment gateway otomatis
- billing otomatis terintegrasi bank
- multi-parent per member
- mobile native app
- fitur marketing website yang kompleks
- reporting lanjutan
- otomasi promosi level

## Success Criteria

MVP dianggap berhasil jika:
- registrasi member berjalan dari public sampai verifikasi admin
- admin dapat mengelola pembayaran bulanan dengan jelas
- coach dapat mencatat attendance dan progress tanpa proses manual terpisah
- member dan orang tua dapat memantau perkembangan dan pembayaran
- admin memiliki dashboard ringkas kondisi operasional club

## Open Questions

Masih perlu diputuskan pada tahap berikutnya:
- field mana milik member dan field mana milik orang tua
- apakah public memilih `program`, `level`, atau keduanya saat registrasi
- detail struktur kurikulum dan checklist skill per level
- periodisasi input progress: per sesi, mingguan, atau model lain
- detail metrik dashboard pembayaran dan level

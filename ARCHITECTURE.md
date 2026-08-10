# Architecture

## Tujuan

Dokumen ini menyimpan keputusan teknis awal yang cukup stabil untuk repo frontend `Allstar`.

## Arsitektur Tingkat Tinggi

Frontend adalah web app yang menjadi antarmuka untuk:
- public
- member
- parent
- coach
- admin

Frontend bertugas:
- menampilkan flow sesuai role
- mengelola state UI
- memanggil backend API
- menjaga validasi dasar di sisi klien

Frontend tidak menjadi sumber business rule utama. Rule domain inti tetap berada di backend.

## Prinsip Desain

- Routing dan akses layar harus berbasis role.
- Semua flow penting harus punya loading, empty, error, dan success state.
- UI hanya menyimpan state presentasional dan state interaksi.
- Data bisnis utama diambil dari backend dan tidak diduplikasi secara liar di client.
- Form yang sensitif tetap harus divalidasi ulang di backend.

## Area Aplikasi

Frontend MVP dibagi menjadi area:
- `public`
- `member`
- `parent`
- `coach`
- `admin`

Struktur halaman disarankan:

```text
src/
  pages/
    public/
    member/
    parent/
    coach/
    admin/
  features/
    auth/
    registrations/
    members/
    payments/
    attendance/
    progress/
    dashboard/
  components/
  services/
  lib/
  styles/
```

Makna area:
- `pages/`: entry route per role atau per halaman
- `features/`: state, hook, form logic, dan UI domain per fitur
- `components/`: komponen reusable
- `services/`: API client dan adapter request/response
- `lib/`: helper umum

## Routing Strategy

Routing sebaiknya dipisah per role:
- public route
- authenticated route
- role-gated route

Contoh area route:
- `/`
- `/register`
- `/login`
- `/member/*`
- `/parent/*`
- `/coach/*`
- `/admin/*`

Aturan:
- user yang belum login tidak boleh mengakses area private
- user login tidak boleh masuk area role lain
- redirect harus jelas dan tidak membingungkan

## Auth Flow

Flow auth MVP:
1. Public registrasi.
2. Akun dibuat dengan status `pending`.
3. Admin memverifikasi registrasi.
4. Setelah aktif, user bisa login sesuai role.

Implikasi frontend:
- harus ada tampilan status `pending verification`
- login flow harus menangani akun belum aktif
- setiap area role harus memuat guard yang jelas

## Role-Based Experience

### Public
- melihat informasi dasar club
- mengisi form registrasi
- memilih program atau level

### Member
- melihat profil
- melihat level aktif
- melihat attendance
- melihat progress
- melihat pembayaran

### Parent
- melihat data anak
- melihat attendance anak
- melihat progress anak
- melihat pembayaran anak

### Coach
- melihat daftar member berdasarkan level yang ditugaskan
- mencatat attendance
- mengisi checklist skill
- memperbarui progress kurikulum

### Admin
- memverifikasi registrasi
- mengelola member
- mengelola pembayaran
- melihat dashboard

## Data Fetching Strategy

Frontend harus memakai service layer untuk semua request ke backend.

Prinsip:
- jangan panggil endpoint langsung dari komponen presentasional
- normalisasi response seperlunya di layer `services/`
- pisahkan state server dan state UI

Contoh service:
- `authService`
- `registrationService`
- `memberService`
- `paymentService`
- `attendanceService`
- `progressService`
- `dashboardService`

## Form Strategy

Form utama MVP:
- registrasi
- login
- verifikasi registrasi
- input pembayaran
- attendance input
- progress checklist

Prinsip:
- validasi dasar dilakukan di client
- error API harus ditampilkan dengan jelas
- field penting harus dipetakan ke model backend secara konsisten

## UI Modules MVP

### Registrasi dan Verifikasi
- halaman registrasi public
- halaman status registrasi
- daftar registrasi untuk admin
- detail registrasi untuk admin

### Member Management
- daftar member untuk admin
- detail member
- ringkasan profil untuk member dan parent

### Pembayaran
- daftar tagihan atau pembayaran
- status pembayaran member
- pencatatan pembayaran manual untuk admin

### Attendance dan Progress
- daftar member per level untuk coach
- form attendance per sesi
- checklist skill per member
- tampilan progres untuk member dan parent

### Dashboard Admin
- card jumlah member
- card ringkasan pembayaran
- distribusi member per level

## State Management

Pisahkan state menjadi:
- `auth state`
- `server state`
- `form state`
- `local UI state`

Aturan:
- auth state global
- server state dikelola per feature
- hindari global store untuk semua hal jika belum dibutuhkan

## Error and Empty States

Semua layar utama harus menangani:
- loading
- unauthorized
- forbidden
- not found
- empty list
- submit failed

Ini penting karena aplikasi banyak bergantung pada data role-based dan status bisnis.

## Frontend Security Baseline

- jangan simpan secret di client
- semua permission final tetap mengandalkan backend
- sembunyikan route dan aksi yang tidak relevan untuk role tertentu
- tangani session expired dengan jelas

## API Boundary

Frontend hanya mengetahui kontrak API, bukan detail penyimpanan database.

Jangan:
- menebak business rule penting di UI
- menghitung ulang status pembayaran dengan logika berbeda dari backend
- menyimpan state domain yang bisa bertentangan dengan server

## Testing Strategy

Prioritas test frontend:
- rendering test untuk halaman inti
- interaction test untuk form penting
- flow test untuk role utama bila stack mendukung

Area minimum yang wajib dites:
- registrasi public
- login dan status pending
- dashboard admin
- input attendance coach
- input progress coach
- tampilan pembayaran member atau parent

## Deployment Target

Belum dikunci. Asumsi sementara:
- frontend dideploy terpisah dari backend
- konfigurasi endpoint API disediakan via environment
- build production harus mendukung routing dan role-based entry yang stabil

## Decision Log

```md
Date: 2026-08-10
Decision: Frontend dibagi per role dan per feature.
Context: Sistem memiliki public, member, parent, coach, dan admin.
Options Considered: struktur per route saja, struktur per role, struktur campuran role-feature
Why: Mempermudah scaling fitur tanpa mencampur semua flow dalam satu area.
Impact: Struktur folder dan ownership komponen menjadi lebih jelas.
```

```md
Date: 2026-08-10
Decision: Business rule utama tetap berada di backend.
Context: Banyak status dan permission penting bergantung pada domain data yang sama.
Options Considered: rule di client, rule di backend, campuran
Why: Mencegah inkonsistensi perilaku antar role dan antar layar.
Impact: Frontend fokus pada pengalaman pengguna dan validasi dasar.
```

```md
Date: 2026-08-10
Decision: Area coach dan admin diperlakukan sebagai first-class flow dalam MVP.
Context: Attendance, progress, verifikasi, dan pembayaran adalah inti operasional produk.
Options Considered: fokus ke member saja, fokus ke admin saja, multi-role MVP
Why: Nilai produk bergantung pada koneksi antar semua role utama.
Impact: Routing dan guard role harus dirancang sejak awal.
```

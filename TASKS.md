# Tasks

Dokumen ini menjadi ringkasan backlog implementasi MVP frontend untuk `Allstar`. Issue GitHub tetap menjadi artefak kerja resmi, tetapi file ini dipakai sebagai peta prioritas.

## Current Priority

Fase implementasi pertama frontend:
- fondasi project frontend
- auth dan route guard dasar
- registrasi public
- admin flow untuk verifikasi registrasi dan pembayaran
- coach flow untuk attendance dan progress
- member dan parent flow untuk monitoring

## Active

- [ ] Tentukan stack frontend dasar dan struktur project
- [ ] Definisikan routing area `public`, `member`, `parent`, `coach`, `admin`
- [ ] Definisikan service layer untuk integrasi ke backend API

## Next

### Milestone 1: Project Foundation

- [ ] Inisialisasi project frontend dan struktur folder sesuai `ARCHITECTURE.md`
- [ ] Setup routing dasar
- [ ] Setup layout dasar per area aplikasi
- [ ] Setup API client dasar
- [ ] Setup auth state dasar
- [ ] Setup error, loading, dan empty state baseline

### Milestone 2: Public dan Auth

- [ ] Buat halaman landing atau public entry minimum
- [ ] Buat halaman registrasi public
- [ ] Buat halaman login
- [ ] Buat halaman status akun `pending verification`
- [ ] Hubungkan form registrasi ke backend
- [ ] Hubungkan login flow ke backend

### Milestone 3: Admin Core Flow

- [ ] Buat daftar registrasi untuk admin
- [ ] Buat detail registrasi untuk admin
- [ ] Buat aksi verifikasi registrasi
- [ ] Buat daftar member untuk admin
- [ ] Buat ringkasan dashboard admin

### Milestone 4: Pembayaran

- [ ] Buat daftar invoice atau pembayaran untuk admin
- [ ] Buat form pencatatan pembayaran manual
- [ ] Buat tampilan status pembayaran untuk member
- [ ] Buat tampilan status pembayaran untuk parent

### Milestone 5: Coach Flow

- [ ] Buat daftar member per level untuk coach
- [ ] Buat halaman atau form attendance per sesi
- [ ] Buat form checklist skill
- [ ] Buat form update progress kurikulum

### Milestone 6: Member dan Parent Flow

- [ ] Buat dashboard ringkas member
- [ ] Buat tampilan attendance member
- [ ] Buat tampilan progress member
- [ ] Buat dashboard ringkas parent
- [ ] Buat tampilan progress anak untuk parent
- [ ] Buat tampilan pembayaran anak untuk parent

### Milestone 7: Hardening

- [ ] Tambahkan route guard per role
- [ ] Review semua empty dan error state
- [ ] Tambahkan test untuk registrasi public
- [ ] Tambahkan test untuk login dan pending state
- [ ] Tambahkan test untuk flow admin utama
- [ ] Tambahkan test untuk flow coach utama

## Suggested First Issues

Issue pertama yang paling layak dibuat:

1. `Setup frontend project foundation`
2. `Define role-based routing and auth shell`
3. `Implement public registration flow`
4. `Implement admin registration verification flow`
5. `Implement admin payment monitoring UI`

## Definition of Done Per Task

Setiap task implementasi dianggap selesai jika:
- ada issue atau PR yang jelas
- layar atau flow yang diubah punya loading, error, dan success state yang layak
- integrasi ke backend terdokumentasi
- test relevan ditambahkan atau ada catatan jujur jika belum tersedia
- tidak ada blocker review

## Done

- [x] Setup workflow GitHub-ready untuk `Team Onyet`
- [x] Lengkapi `PRODUCT.md`
- [x] Lengkapi `ARCHITECTURE.md`

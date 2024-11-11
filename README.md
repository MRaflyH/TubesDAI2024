## Deskripsi

**Magic Cube Replay** adalah aplikasi web interaktif yang memungkinkan pengguna untuk melihat replay dari konfigurasi Magic Cube (Rubik's Cube) menggunakan berbagai algoritma penyelesaian seperti Hill Climbing dan Genetic Algorithm. Proyek ini dikembangkan sebagai bagian dari tugas bonus dan menggabungkan frontend yang dinamis dengan backend yang kuat untuk memberikan pengalaman visual yang menarik.

Anda dapat mengakses aplikasi ini melalui tautan berikut:
[https://magic-cube-replay.vercel.app/](https://magic-cube-replay.vercel.app/)

## Fitur

- **Visualisasi 3D Magic Cube:** Melihat konfigurasi Magic Cube secara real-time dengan rendering 3D.
- **Replay Algoritma Penyelesaian:** Menampilkan langkah-langkah penyelesaian menggunakan algoritma seperti:
  - Steepest Ascent Hill Climbing
  - Random Restart Hill Climbing
  - Stochastic Hill Climbing
  - Simulated Annealing
  - Genetic Algorithm
- **Kontrol Playback:** Mengatur kecepatan replay, memulai/menjeda, dan navigasi melalui langkah-langkah penyelesaian.
- **Pemilihan Algoritma:** Memilih algoritma penyelesaian yang diinginkan dari dropdown menu.

## Teknologi yang Digunakan

### Frontend

- **React.js:** Library JavaScript untuk membangun antarmuka pengguna.
- **Three.js & @react-three/fiber:** Untuk rendering grafis 3D interaktif.
- **Axios:** Untuk melakukan permintaan HTTP ke backend.

### Backend

- **FastAPI:** Framework Python untuk membangun API yang cepat dan efisien.
- **Uvicorn:** Server ASGI untuk menjalankan aplikasi FastAPI.
- **Mangum:** Adapter untuk menjalankan aplikasi ASGI di lingkungan serverless seperti Vercel.

### Deployment

- **Vercel:** Platform untuk menghosting frontend dan backend (Serverless Functions).

## Cara Menggunakan

1. **Kunjungi Website:**
   Buka [Magic Cube Replay](https://magic-cube-replay.vercel.app/) di browser Anda.

2. **Pilih Algoritma:**
   Dari dropdown menu, pilih algoritma penyelesaian yang ingin Anda gunakan.

3. **Mulai Replay:**
   Klik tombol "Play" untuk memulai replay penyelesaian Magic Cube. Anda dapat mengatur kecepatan replay sesuai keinginan.

4. **Navigasi Replay:**
   Gunakan kontrol playback untuk menjeda, memutar, atau menavigasi melalui langkah-langkah penyelesaian.

## Cara Mengembangkan dan Menjalankan Secara Lokal

### Prasyarat

- **Node.js & npm:** Untuk menjalankan frontend.
- **Python 3.8+ & pip:** Untuk menjalankan backend.

### Frontend

1. **Clone Repository:**
   ```bash
   git clone https://github.com/username/magic-cube-replay.git
   cd magic-cube-replay/frontend
# 🌐 Tor-Termux IP Rotator

**Tool otomatis untuk mengubah IP address secara instant menggunakan Tor di Termux!**

Tor-Termux adalah aplikasi Python sederhana yang memudahkan kamu untuk merotasi IP address secara otomatis setiap beberapa detik. Sempurna untuk testing, privasi, atau keperluan lainnya tanpa ribet!

## ⚡ Fitur Utama

- **Rotasi IP Otomatis** - Ubah IP setiap 3 detik dengan sekali klik
- **Proxy SOCKS5** - Menggunakan protokol SOCKS5 melalui Tor untuk keamanan maksimal
- **Sederhana & Cepat** - Tidak perlu konfigurasi rumit, langsung bisa dipakai
- **Menu Interaktif** - Interface user-friendly yang mudah digunakan
- **Informasi Lengkap** - Tampilkan IP, negara, dan ISP setiap rotasi
- **Kontrol Penuh** - Start/stop kapan saja dengan mudah

## 📋 Persyaratan

Sebelum menggunakan Tor-Termux, pastikan kamu memiliki:

- **Termux** (aplikasi terminal di Android)
- **Python 3.x** (biasanya sudah terinstal di Termux)
- **Tor** (akan kita install)
- **Internet Connection** (tentunya!)

## 🚀 Cara Instalasi

### 1. Buka Termux dan Update Paket

```bash
pkg update && pkg upgrade -y
```

### 2. Install Tor

```bash
pkg install tor -y
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install pysocks requests
```

### 4. Download/Clone Repository

Jika sudah ada Git:

```bash
git clone https://github.com/8782hei-sketch/Tor-termux.git
cd Tor-termux
```

Atau download file `tor.py` langsung ke Termux.

### 5. Jalankan Script

```bash
python tor.py
```

## 📖 Cara Penggunaan

### Langkah-langkah Penggunaan:

1. **Jalankan aplikasi:**
   ```bash
   python tor.py
   ```

2. **Pilih menu "1. Start IP Rotator"** dari tampilan awal

3. **Biarkan berjalan!** Script akan:
   - ✅ Memulai daemon Tor
   - ✅ Menampilkan IP publik kamu
   - ✅ Otomatis mengubah IP setiap 3 detik
   - ✅ Menampilkan negara dan ISP untuk setiap IP

4. **Tekan `Ctrl+C`** untuk menghentikan rotasi

5. **Pilih menu "2. Exit"** untuk keluar total

### Contoh Output:

```
[12:34:56] IP Saat Ini : 123.45.67.89 [United States, ISPNameHere]
           ↳ Meminta sirkuit baru...

[12:34:59] IP Saat Ini : 234.56.78.90 [Netherlands, SomeISP]
           ↳ Meminta sirkuit baru...

[12:35:02] IP Saat Ini : 45.67.89.01 [Germany, AnotherISP]
           ↳ Meminta sirkuit baru...
```

## 🔧 Troubleshooting

### ❌ Error: "Tor tidak ditemukan"

**Solusi:**
```bash
pkg install tor -y
```

### ❌ Error: "requests tidak ditemukan"

**Solusi:**
```bash
pip install requests
```

### ❌ Error: "PySocks tidak ditemukan"

**Solusi:**
```bash
pip install pysocks
```

### ❌ Tor tidak bisa bootstrap

- Pastikan internet terhubung dengan baik
- Coba tunggu beberapa saat (Tor butuh waktu untuk connect)
- Coba restart Termux dan jalankan lagi

### ❌ IP tidak berubah-ubah

- Pastikan Tor sudah fully connected (tunggu bootstrap complete)
- Cek koneksi internet kamu
- Coba force stop dan jalankan ulang

## ⚙️ Konfigurasi (Opsional)

Jika ingin mengubah pengaturan, buka file `tor.py` dan ubah bagian berikut:

```python
TOR_SOCKS_PORT   = 9050          # Port SOCKS (standar)
TOR_CONTROL_PORT = 9051          # Port Control (standar)
PASSWORD         = "tortermux"    # Password kontrol (bisa diganti)
```

Untuk mengubah frekuensi rotasi, cari baris:
```python
time.sleep(3)  # Ganti 3 dengan angka detik yang diinginkan
```

## 📝 Struktur File

```
Tor-termux/
├── tor.py                 # Script utama
├── requirements.txt       # Python dependencies
└── README.md             # File ini
```

## ⚠️ Disclaimer

Tool ini dibuat untuk tujuan **edukatif dan testing pribadi**. 

- Gunakan dengan bertanggung jawab
- Jangan gunakan untuk aktivitas ilegal atau mencurigakan
- Ketahui regulasi jaringan tempat kamu tinggal
- Tor adalah teknologi privasi yang legitimate

## 🤝 Kontribusi

Punya saran atau menemukan bug? Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Project ini bebas digunakan untuk keperluan pribadi dan edukasi.

## 💬 Support

Jika ada pertanyaan atau masalah:
- Buka GitHub Issues
- Pastikan semua dependencies sudah terinstall
- Cek koneksi internet kamu
- Coba perhatikan error message yang muncul

---

**Made with ❤️ for Termux users**

Happy IP Rotating! 🎉

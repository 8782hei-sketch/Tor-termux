#!/usr/bin/env python3
"""
Tor Termux - IP Rotator
=======================
Script ini menjalankan Tor, mengambil IP melalui proxy SOCKS5,
dan mengirim sinyal NEWNYM setiap 3 detik untuk mengubah identitas.

Kebutuhan:
  - Termux dengan Python3
  - Tor        : pkg install tor
  - requests   : pip install requests
  - PySocks    : pip install requests[socks]   (atau pip install pysocks)

Jalankan: python tor_termux.py
"""

import os
import sys
import time
import socket
import subprocess
import signal

# ============================================================
# Konfigurasi
# ============================================================
TOR_SOCKS_PORT   = 9050
TOR_CONTROL_PORT = 9051
PASSWORD         = "tortermux"          # password kontrol (bebas)
TOR_DATA_DIR     = os.path.expanduser("~/.tor_termux_data")

# Proses tor yang berjalan (global)
tor_process = None

# ============================================================
# Fungsi banner
# ============================================================
def print_banner():
    banner = r"""
    {GREEN}
       _____   ____    _____     _____  ______  __   __  __   __  _   __
      |_   _| / __ \ |  __ \   |_   _||  ____||  \ /  ||  | |  || | / /
        | |  | |  | || |__) |    | |  | |__   |   V   ||  | |  || |/ /
        | |  | |  | ||  _  /     | |  |  __|  | |\ /| ||  | |  ||   /
        | |  | |__| || | \ \     | |  | |____ | |   | ||  |_|  || |\ \
        |_|   \____/ |_|  \_\    |_|  |______||_|   |_||______||_| \_\
    {RESET}
    {CYAN}     ____  _               _        __
    {RESET}
    """.format(GREEN='\033[92m', CYAN='\033[96m', RESET='\033[0m')
    print(banner)

# ============================================================
# Cek dependensi
# ============================================================
def check_dependencies():
    # Cek tor
    if subprocess.call(["which", "tor"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL) != 0:
        sys.exit("\033[91m[!] Tor tidak ditemukan. Install dengan 'pkg install tor'\033[0m")

    # Cek requests
    try:
        import requests
    except ImportError:
        sys.exit("\033[91m[!] requests tidak ditemukan. Install dengan 'pip install requests'\033[0m")

    # Cek dukungan socks (PySocks)
    try:
        import socks
    except ImportError:
        sys.exit("\033[91m[!] PySocks tidak ditemukan. Install dengan 'pip install requests[socks]'\033[0m")

# ============================================================
# Generate password hash untuk kontrol Tor
# ============================================================
def generate_hashed_password(password):
    result = subprocess.run(
        ["tor", "--hash-password", password],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError("Gagal menghasilkan hash password Tor")
    # Output berisi baris seperti "16:ABCD..."
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("16:"):
            return line
    raise RuntimeError("Format hash tidak dikenali")

# ============================================================
# Tunggu bootstrap Tor
# ============================================================
def wait_for_bootstrap():
    print("[*] Menunggu Tor bootstrap...")
    for _ in range(30):   # max 30 detik
        try:
            s = socket.create_connection(("127.0.0.1", TOR_CONTROL_PORT), timeout=2)
            # Otentikasi
            s.sendall(f'AUTHENTICATE "{PASSWORD}"\r\n'.encode())
            resp = s.recv(4096).decode()
            if "250 OK" not in resp:
                s.close()
                time.sleep(1)
                continue

            # Cek status bootstrap
            s.sendall(b"GETINFO status/bootstrap-phase\r\n")
            resp = s.recv(4096).decode()
            s.close()
            if "PROGRESS=100" in resp:
                print("\033[92m[✓] Tor telah terhubung ke jaringan.\033[0m")
                return True
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Tor gagal bootstrap setelah 30 detik")

# ============================================================
# Mulai proses Tor
# ============================================================
def start_tor():
    global tor_process
    if tor_process is not None:
        print("[*] Tor sudah berjalan.")
        return

    if not os.path.exists(TOR_DATA_DIR):
        os.makedirs(TOR_DATA_DIR)

    hashed = generate_hashed_password(PASSWORD)
    cmd = [
        "tor",
        "--SOCKSPort", str(TOR_SOCKS_PORT),
        "--ControlPort", str(TOR_CONTROL_PORT),
        "--HashedControlPassword", hashed,
        "--DataDirectory", TOR_DATA_DIR,
        "--RunAsDaemon", "0"         # berjalan di foreground, kita kendalikan
    ]
    print("[*] Memulai Tor...")
    tor_process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    wait_for_bootstrap()

# ============================================================
# Hentikan proses Tor
# ============================================================
def stop_tor():
    global tor_process
    if tor_process:
        print("[*] Menghentikan Tor...")
        tor_process.terminate()
        try:
            tor_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tor_process.kill()
        tor_process = None

# ============================================================
# Kirim sinyal NEWNYM ke kontrol Tor
# ============================================================
def send_newnym():
    try:
        s = socket.create_connection(("127.0.0.1", TOR_CONTROL_PORT), timeout=5)
        # Otentikasi
        s.sendall(f'AUTHENTICATE "{PASSWORD}"\r\n'.encode())
        resp = s.recv(4096).decode()
        if "250 OK" not in resp:
            s.close()
            return False
        # Kirim sinyal NEWNYM
        s.sendall(b"SIGNAL NEWNYM\r\n")
        resp = s.recv(4096).decode()
        s.close()
        if "250 OK" in resp:
            return True
    except Exception as e:
        print(f"\033[93m[!] Gagal mengirim NEWNYM: {e}\033[0m")
    return False

# ============================================================
# Ambil IP publik saat ini melalui Tor (SOCKS5)
# ============================================================
def get_current_ip():
    try:
        import requests
        proxies = {
            'http':  f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
            'https': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}'
        }
        # Gunakan API sederhana (HTTP) agar kompatibel
        resp = requests.get('http://ip-api.com/json', proxies=proxies, timeout=10)
        data = resp.json()
        ip      = data.get('query', 'N/A')
        country = data.get('country', '??')
        isp     = data.get('isp', '??')
        return f"{ip} [{country}, {isp}]"
    except Exception:
        return "Gagal mengambil IP"

# ============================================================
# Menu utama
# ============================================================
def main_menu():
    print_banner()
    print(" \033[93mMenu:\033[0m")
    print("   \033[92m1. Start IP Rotator\033[0m")
    print("   \033[91m2. Exit\033[0m")
    while True:
        try:
            pilihan = input("\nPilih (1/2): ").strip()
            if pilihan == '1':
                return True
            elif pilihan == '2':
                return False
            else:
                print("Masukkan 1 atau 2.")
        except KeyboardInterrupt:
            print("\n")
            return False

# ============================================================
# Rotasi IP
# ============================================================
def run_rotator():
    global tor_process
    try:
        # Pastikan Tor berjalan
        if tor_process is None:
            start_tor()

        print("\n\033[93m[*] Rotasi IP dimulai. Tekan Ctrl+C untuk kembali ke menu.\033[0m\n")
        while True:
            # Tampilkan IP saat ini
            current = get_current_ip()
            print(f"[{time.strftime('%H:%M:%S')}] IP Saat Ini : {current}")

            # Minta sirkuit baru
            if send_newnym():
                print("             ↳ Meminta sirkuit baru...")
            else:
                print("             ↳ \033[91mGagal mengganti sirkuit!\033[0m")

            # Tunggu 3 detik
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n\033[93m[*] Dihentikan oleh pengguna. Kembali ke menu.\033[0m")
    # Tor tetap berjalan, bisa di-start lagi tanpa inisialisasi ulang

# ============================================================
# Pembersihan saat keluar
# ============================================================
def cleanup():
    stop_tor()
    print("\033[92mSampai jumpa!\033[0m")

# ============================================================
# Fungsi utama
# ============================================================
def main():
    try:
        check_dependencies()
        while True:
            if not main_menu():
                break
            run_rotator()
    except KeyboardInterrupt:
        print("\n[*] Keluar paksa...")
    finally:
        cleanup()

# ============================================================
if __name__ == "__main__":
    main()
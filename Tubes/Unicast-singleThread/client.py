"""
UNICAST A -> B | SINGLE THREAD
Client Side
"""

import socket # coms antar jaringan
import os # akses file
import struct # conv biner
import json # encode/decode

# Config
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090
BUFFER = 4096 # 4KB

# Warna CLI
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"

def banner():
    print(f"""
{CYAN}{BOLD}
CLIENT SIDE
{RESET}
Target : {SERVER_HOST}:{SERVER_PORT}
""")

# Helper: Kirim header + payload
def send_header(sock, header_dict):
    # Kirim header JSON dengan prefix 4-byte panjang
    hdr_bytes = json.dumps(header_dict).encode("utf-8") # Convert dictionary → JSON → bytes
    sock.sendall(struct.pack(">I", len(hdr_bytes))) # Kirim panjang header
    sock.sendall(hdr_bytes) # Kirim isi header

def send_signal_done(sock):
    # Kirim sinyal selesai (header length = 0)
    sock.sendall(struct.pack(">I", 0))

# Kirim Teks
def send_text(sock, text, subtype):
    # subtype: 'words' | 'sentence' | 'paragraph'
    payload = text.encode("utf-8")
    header = {
        "type":    "text",
        "subtype": subtype,
        "length":  len(payload),
    }
    send_header(sock, header)
    sock.sendall(payload)

    label_map = {
        "words":     "KATA (1-5 kata)",
        "sentence":  "KALIMAT PANJANG",
        "paragraph": "PARAGRAF",
    }
    print(f"  {GREEN}[✓] Terkirim {label_map[subtype]}: \"{text}\"{RESET}")

# Kirim File
def send_file(sock, filepath, filetype):
    # filetype: 'document' | 'image' | 'audio' | 'video'
    if not os.path.isfile(filepath):
        print(f"  {RED}[✗] File tidak ditemukan: {filepath}{RESET}")
        return False

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    header = {
        "type":     "file",
        "filetype": filetype,
        "filename": filename,
        "filesize": filesize,
    }
    send_header(sock, header)

    sent = 0
    with open(filepath, "rb") as f: # rb = read binary
        while True:
            chunk = f.read(BUFFER) # Baca per chuck
            if not chunk:
                break
            sock.sendall(chunk)
            sent += len(chunk)
            pct = int(sent / filesize * 40)
            bar = "█" * pct + "░" * (40 - pct)
            print(f"\r  [{bar}] {sent}/{filesize} byte", end="", flush=True)

    print()
    type_label = {
        "document": "DOKUMEN",
        "image":    "GAMBAR",
        "audio":    "AUDIO",
        "video":    "VIDEO",
    }.get(filetype, "FILE")
    print(f"  {GREEN}[✓] Terkirim {type_label}: {filename} ({filesize:,} byte){RESET}")
    return True

# Deteksi Tipe File
def detect_filetype(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".txt", ".docx", ".pdf"]:
        return "document"
    elif ext in [".jpg", ".jpeg", ".png"]:
        return "image"
    elif ext in [".mp3"]:
        return "audio"
    elif ext in [".mp4"]:
        return "video"
    return None

# Menu Utama
def show_menu():
    print(f"""
{BOLD}{YELLOW}══════════════ MENU PENGIRIMAN ══════════════{RESET}
 {BLUE}[1]{RESET} Kirim 1-5 Kata
 {BLUE}[2]{RESET} Kirim 1 Kalimat Panjang
 {BLUE}[3]{RESET} Kirim 1 Paragraf
 {BLUE}[4]{RESET} Kirim Dokumen (.txt / .docx / .pdf)
 {BLUE}[5]{RESET} Kirim Gambar  (.jpg / .png)
 {BLUE}[6]{RESET} Kirim Audio   (.mp3)
 {BLUE}[7]{RESET} Kirim Video   (.mp4)
 {BLUE}[0]{RESET} Keluar & Tutup Koneksi
{BOLD}{YELLOW}════════════════════════════════════════════{RESET}
""")

def input_words():
    while True:
        raw = input(f"  {DIM}Masukkan 1-5 kata: {RESET}").strip()
        words = raw.split()
        if 1 <= len(words) <= 5:
            return raw
        print(f"  {RED}[!] Harus 1 sampai 5 kata. Anda memasukkan {len(words)} kata.{RESET}")

def input_filepath(allowed_exts):
    while True:
        path = input(f"  {DIM}Path file ({', '.join(allowed_exts)}): {RESET}").strip()
        if not path:
            continue
        ext = os.path.splitext(path)[1].lower()
        if ext not in allowed_exts:
            print(f"  {RED}[!] Ekstensi harus salah satu dari: {', '.join(allowed_exts)}{RESET}")
            continue
        if not os.path.isfile(path):
            print(f"  {RED}[!] File tidak ditemukan: {path}{RESET}")
            continue
        return path

# Main
def main():
    banner()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
        sock.connect((SERVER_HOST, SERVER_PORT))
        print(f"{GREEN}[+] Terhubung ke Node B ({SERVER_HOST}:{SERVER_PORT}){RESET}")
    except ConnectionRefusedError:
        print(f"{RED}[✗] Gagal terhubung. Pastikan server.py sudah berjalan di Node B.{RESET}")
        return

    try:
        while True:
            show_menu()
            choice = input(f"  Pilih menu: ").strip()

            if choice == "1":
                text = input_words()
                send_text(sock, text, "words")

            elif choice == "2":
                text = input(f"  {DIM}Masukkan kalimat panjang: {RESET}").strip()
                if text:
                    send_text(sock, text, "sentence")

            elif choice == "3":
                print(f"  {DIM}Masukkan paragraf (akhiri dengan baris kosong):{RESET}")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                text = " ".join(lines)
                if text:
                    send_text(sock, text, "paragraph")

            elif choice == "4":
                path = input_filepath([".txt", ".docx", ".pdf"])
                send_file(sock, path, "document")

            elif choice == "5":
                path = input_filepath([".jpg", ".jpeg", ".png"])
                send_file(sock, path, "image")

            elif choice == "6":
                path = input_filepath([".mp3"])
                send_file(sock, path, "audio")

            elif choice == "7":
                path = input_filepath([".mp4"])
                send_file(sock, path, "video")

            elif choice == "0":
                print(f"\n{YELLOW}[*] Menutup koneksi ...{RESET}")
                send_signal_done(sock)
                break

            else:
                print(f"  {RED}[!] Pilihan tidak valid.{RESET}")

    except (BrokenPipeError, ConnectionResetError):
        print(f"\n{RED}[!] Koneksi ke server terputus.{RESET}")
    finally:
        sock.close()
        print(f"{CYAN}[-] Socket ditutup. Program selesai.{RESET}")

main()
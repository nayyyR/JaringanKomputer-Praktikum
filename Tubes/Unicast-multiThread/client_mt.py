"""
UNICAST A -> B | MULTI THREAD
CLIENT SIDE
"""

import socket
import os
import struct
import json
import threading
import time

# Config
SERVER_HOST = '127.0.0.1'   # Ganti dengan IP Node B
SERVER_PORT = 9090
BUFFER      = 4096

# Warna CLI 
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
RED     = "\033[91m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
DIM     = "\033[2m"

print_lock = threading.Lock()

def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║    UNICAST A → B  |  MULTI THREAD  |  NODE A        ║
║             CLIENT (PENGIRIM)                        ║
╚══════════════════════════════════════════════════════╝{RESET}
  Target : {SERVER_HOST}:{SERVER_PORT}
  Mode   : Setiap pengiriman berjalan di thread sendiri
""")

def tprint(*args, tid=None, **kwargs):
    prefix = f"{DIM}[T-{tid:02d}]{RESET} " if tid is not None else ""
    with print_lock:
        print(prefix + " ".join(str(a) for a in args), **kwargs)

# Koneksi Per Thread
def make_connection():
    """Buka koneksi TCP baru ke server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    return sock

# Hepler Kirim
def send_header(sock, header_dict):
    hdr_bytes = json.dumps(header_dict).encode("utf-8")
    sock.sendall(struct.pack(">I", len(hdr_bytes)))
    sock.sendall(hdr_bytes)

def send_done(sock):
    sock.sendall(struct.pack(">I", 0))

# Worker Func (dijalankan di thread)
def worker_text(text, subtype, tid):
    """Thread worker: kirim teks."""
    try:
        sock = make_connection()
        payload = text.encode("utf-8")
        send_header(sock, {"type": "text", "subtype": subtype, "length": len(payload)})
        sock.sendall(payload)
        send_done(sock)
        sock.close()

        label_map = {
            "words":     "KATA",
            "sentence":  "KALIMAT",
            "paragraph": "PARAGRAF",
        }
        tprint(f"{GREEN}[✓] Thread selesai — {label_map[subtype]}: \"{text[:50]}\"...{RESET}"
               if len(text) > 50 else
               f"{GREEN}[✓] Thread selesai — {label_map[subtype]}: \"{text}\"{RESET}", tid=tid)
    except Exception as e:
        tprint(f"{RED}[✗] Thread error: {e}{RESET}", tid=tid)

def worker_file(filepath, filetype, tid):
    """Thread worker: kirim file."""
    try:
        if not os.path.isfile(filepath):
            tprint(f"{RED}[✗] File tidak ditemukan: {filepath}{RESET}", tid=tid)
            return

        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)

        sock = make_connection()
        send_header(sock, {
            "type":     "file",
            "filetype": filetype,
            "filename": filename,
            "filesize": filesize,
        })

        sent = 0
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(BUFFER)
                if not chunk:
                    break
                sock.sendall(chunk)
                sent += len(chunk)
                pct = int(sent / filesize * 30)
                bar = "█" * pct + "░" * (30 - pct)
                with print_lock:
                    print(f"\r  [T-{tid:02d}] [{bar}] {sent}/{filesize} byte", end="", flush=True)

        with print_lock:
            print()

        send_done(sock)
        sock.close()

        type_label = {
            "document": "DOKUMEN",
            "image":    "GAMBAR",
            "audio":    "AUDIO",
            "video":    "VIDEO",
        }.get(filetype, "FILE")
        tprint(f"{GREEN}[✓] Thread selesai — {type_label}: {filename} ({filesize:,} byte){RESET}", tid=tid)

    except Exception as e:
        tprint(f"{RED}[✗] Thread error: {e}{RESET}", tid=tid)

# Mode Pengiriman
def send_sequential(tasks):
    """
    Kirim task satu per satu (tapi masing-masing via thread sendiri).
    Thread berikutnya dimulai setelah thread sebelumnya selesai.
    """
    print(f"\n{YELLOW}[~] Mode: SEQUENTIAL THREAD{RESET}")
    for i, (fn, args) in enumerate(tasks, 1):
        tid = i
        tprint(f"{MAGENTA}Memulai thread ...{RESET}", tid=tid)
        t = threading.Thread(target=fn, args=(*args, tid))
        t.start()
        t.join()  # tunggu selesai sebelum mulai berikutnya

def send_parallel(tasks):
    """
    Kirim semua task secara bersamaan (concurrent).
    Semua thread dinyalakan sekaligus, lalu tunggu semua selesai.
    """
    print(f"\n{YELLOW}[~] Mode: PARALLEL THREAD (semua sekaligus){RESET}")
    threads = []
    for i, (fn, args) in enumerate(tasks, 1):
        tid = i
        tprint(f"{MAGENTA}Memulai thread ...{RESET}", tid=tid)
        t = threading.Thread(target=fn, args=(*args, tid))
        threads.append(t)
        t.start()

    print(f"{CYAN}[~] {len(threads)} thread berjalan paralel, menunggu semua selesai...{RESET}\n")
    for t in threads:
        t.join()
    print(f"\n{GREEN}[✓] Semua thread selesai.{RESET}")

# Validasi Input
def input_words():
    while True:
        raw = input(f"  {DIM}Masukkan 1–5 kata: {RESET}").strip()
        words = raw.split()
        if 1 <= len(words) <= 5:
            return raw
        print(f"  {RED}[!] Harus 1–5 kata. Anda memasukkan {len(words)} kata.{RESET}")

def input_filepath(allowed_exts):
    while True:
        path = input(f"  {DIM}Path file ({', '.join(allowed_exts)}): {RESET}").strip()
        if not path:
            continue
        ext = os.path.splitext(path)[1].lower()
        if ext not in allowed_exts:
            print(f"  {RED}[!] Ekstensi harus: {', '.join(allowed_exts)}{RESET}")
            continue
        if not os.path.isfile(path):
            print(f"  {RED}[!] File tidak ditemukan: {path}{RESET}")
            continue
        return path

def detect_filetype(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".txt", ".docx", ".pdf"]:  return "document"
    if ext in [".jpg", ".jpeg", ".png"]:  return "image"
    if ext in [".mp3"]:                   return "audio"
    if ext in [".mp4"]:                   return "video"
    return None

# Menu
def show_menu():
    print(f"""
{BOLD}{YELLOW}══════════════════════════════════════════════════════{RESET}
{BOLD}  MENU PENGIRIMAN  —  UNICAST MULTI THREAD{RESET}
{YELLOW}══════════════════════════════════════════════════════{RESET}
  {BLUE}[1]{RESET} Kirim 1–5 Kata           (1 thread)
  {BLUE}[2]{RESET} Kirim 1 Kalimat Panjang  (1 thread)
  {BLUE}[3]{RESET} Kirim 1 Paragraf         (1 thread)
  {BLUE}[4]{RESET} Kirim Dokumen            (.txt/.docx/.pdf)
  {BLUE}[5]{RESET} Kirim Gambar             (.jpg/.png)
  {BLUE}[6]{RESET} Kirim Audio              (.mp3)
  {BLUE}[7]{RESET} Kirim Video              (.mp4)
  {YELLOW}──────────────────────────────────────────────────────{RESET}
  {MAGENTA}[8]{RESET} Kirim SEMUA sekaligus   {DIM}(parallel — semua tipe){RESET}
  {MAGENTA}[9]{RESET} Kirim SEMUA berurutan   {DIM}(sequential thread){RESET}
  {YELLOW}──────────────────────────────────────────────────────{RESET}
  {BLUE}[0]{RESET} Keluar
{YELLOW}══════════════════════════════════════════════════════{RESET}
""")

def build_all_tasks():
    """Kumpulkan semua input dari user untuk mode kirim semua."""
    print(f"\n{CYAN}[*] Siapkan semua data yang akan dikirim:{RESET}")
    tasks = []

    print(f"\n  {BOLD}--- Teks ---{RESET}")
    w = input_words()
    tasks.append((worker_text, (w, "words")))

    s = input(f"  {DIM}Kalimat panjang: {RESET}").strip()
    if s:
        tasks.append((worker_text, (s, "sentence")))

    print(f"  {DIM}Paragraf (baris kosong = selesai):{RESET}")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    if lines:
        tasks.append((worker_text, (" ".join(lines), "paragraph")))

    print(f"\n  {BOLD}--- File ---{RESET}")
    for label, exts, ftype in [
        ("Dokumen", [".txt", ".docx", ".pdf"], "document"),
        ("Gambar",  [".jpg", ".jpeg", ".png"], "image"),
        ("Audio",   [".mp3"],                  "audio"),
        ("Video",   [".mp4"],                  "video"),
    ]:
        path = input_filepath(exts)
        tasks.append((worker_file, (path, ftype)))

    return tasks

# Main
def main():
    banner()

    # Test koneksi awal
    try:
        test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test.settimeout(3)
        test.connect((SERVER_HOST, SERVER_PORT))
        test.sendall(struct.pack(">I", 0))  # langsung tutup
        test.close()
        print(f"{GREEN}[+] Server Node B dapat dijangkau di {SERVER_HOST}:{SERVER_PORT}{RESET}\n")
    except Exception:
        print(f"{RED}[✗] Tidak dapat terhubung ke {SERVER_HOST}:{SERVER_PORT}. "
              f"Pastikan server_mt.py sudah berjalan.{RESET}")
        return

    tid_counter = [0]

    while True:
        show_menu()
        choice = input("  Pilih menu: ").strip()

        if choice == "1":
            text = input_words()
            tid_counter[0] += 1
            tid = tid_counter[0]
            tprint(f"{MAGENTA}Memulai thread untuk KATA...{RESET}", tid=tid)
            t = threading.Thread(target=worker_text, args=(text, "words", tid))
            t.start(); t.join()

        elif choice == "2":
            text = input(f"  {DIM}Kalimat panjang: {RESET}").strip()
            if text:
                tid_counter[0] += 1; tid = tid_counter[0]
                tprint(f"{MAGENTA}Memulai thread untuk KALIMAT...{RESET}", tid=tid)
                t = threading.Thread(target=worker_text, args=(text, "sentence", tid))
                t.start(); t.join()

        elif choice == "3":
            print(f"  {DIM}Paragraf (baris kosong = selesai):{RESET}")
            lines = []
            while True:
                line = input()
                if line == "": break
                lines.append(line)
            if lines:
                text = " ".join(lines)
                tid_counter[0] += 1; tid = tid_counter[0]
                tprint(f"{MAGENTA}Memulai thread untuk PARAGRAF...{RESET}", tid=tid)
                t = threading.Thread(target=worker_text, args=(text, "paragraph", tid))
                t.start(); t.join()

        elif choice == "4":
            path = input_filepath([".txt", ".docx", ".pdf"])
            tid_counter[0] += 1; tid = tid_counter[0]
            tprint(f"{MAGENTA}Memulai thread untuk DOKUMEN...{RESET}", tid=tid)
            t = threading.Thread(target=worker_file, args=(path, "document", tid))
            t.start(); t.join()

        elif choice == "5":
            path = input_filepath([".jpg", ".jpeg", ".png"])
            tid_counter[0] += 1; tid = tid_counter[0]
            tprint(f"{MAGENTA}Memulai thread untuk GAMBAR...{RESET}", tid=tid)
            t = threading.Thread(target=worker_file, args=(path, "image", tid))
            t.start(); t.join()

        elif choice == "6":
            path = input_filepath([".mp3"])
            tid_counter[0] += 1; tid = tid_counter[0]
            tprint(f"{MAGENTA}Memulai thread untuk AUDIO...{RESET}", tid=tid)
            t = threading.Thread(target=worker_file, args=(path, "audio", tid))
            t.start(); t.join()

        elif choice == "7":
            path = input_filepath([".mp4"])
            tid_counter[0] += 1; tid = tid_counter[0]
            tprint(f"{MAGENTA}Memulai thread untuk VIDEO...{RESET}", tid=tid)
            t = threading.Thread(target=worker_file, args=(path, "video", tid))
            t.start(); t.join()

        elif choice == "8":
            tasks = build_all_tasks()
            send_parallel(tasks)

        elif choice == "9":
            tasks = build_all_tasks()
            send_sequential(tasks)

        elif choice == "0":
            print(f"\n{YELLOW}[*] Keluar dari program.{RESET}")
            print(f"{CYAN}[-] Program selesai.{RESET}")
            break

        else:
            print(f"  {RED}[!] Pilihan tidak valid.{RESET}")

main()
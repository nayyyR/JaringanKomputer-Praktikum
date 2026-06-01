"""
UNICAST A -> B | MULTI THREAD
Server Side
"""

import socket
import os
import struct
import json
import threading

# Config
HOST     = '0.0.0.0'
PORT     = 9090
BUFFER   = 4096
SAVE_DIR = "received_files_mt"

ALLOWED_EXTENSIONS = {
    "document": [".txt", ".docx", ".pdf"],
    "image":    [".jpg", ".jpeg", ".png"],
    "audio":    [".mp3"],
    "video":    [".mp4"],
}

# Warna CLI
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
MAGENTA= "\033[95m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"

# Lock agar output antar thread tidak tumpang tindih
print_lock = threading.Lock()

# Counter thread aktif
active_threads = 0
active_lock    = threading.Lock()

def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║    UNICAST A → B  |  MULTI THREAD  |  NODE B        ║
║             SERVER (PENERIMA)                        ║
╚══════════════════════════════════════════════════════╝{RESET}
  Host : {HOST}   Port : {PORT}
  Save : ./{SAVE_DIR}/
  Mode : Setiap client ditangani thread terpisah
""")

def tprint(*args, tid=None, **kwargs):
    """Thread-safe print dengan label thread ID."""
    prefix = f"{DIM}[T-{tid:02d}]{RESET} " if tid is not None else ""
    with print_lock:
        print(prefix + " ".join(str(a) for a in args), **kwargs)

# Helper
def recv_exact(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(min(BUFFER, length - len(data)))
        if not chunk:
            raise ConnectionError("Koneksi terputus saat menerima data.")
        data += chunk
    return data

def recv_header(conn):
    raw_len  = recv_exact(conn, 4)
    hdr_len  = struct.unpack(">I", raw_len)[0]
    if hdr_len == 0:
        return None  # sinyal selesai
    hdr_bytes = recv_exact(conn, hdr_len)
    return json.loads(hdr_bytes.decode("utf-8"))

# Handler Per Tipe
def handle_text(conn, header, tid, addr):
    subtype = header.get("subtype", "text")
    length  = header["length"]
    payload = recv_exact(conn, length)
    text    = payload.decode("utf-8")

    label_map = {
        "words":     "KATA (1-5 kata)",
        "sentence":  "KALIMAT PANJANG",
        "paragraph": "PARAGRAF",
    }
    label = label_map.get(subtype, "TEKS")
    tprint(f"{GREEN}[✓] TERIMA {label} dari {addr}{RESET}", tid=tid)
    tprint(f'  └─ "{text}"', tid=tid)

def handle_file(conn, header, tid, addr):
    filename = header["filename"]
    filetype = header["filetype"]
    filesize = header["filesize"]
    ext      = os.path.splitext(filename)[1].lower()

    allowed = ALLOWED_EXTENSIONS.get(filetype, [])
    if ext not in allowed:
        tprint(f"{RED}[✗] Ekstensi '{ext}' tidak diizinkan untuk tipe '{filetype}'{RESET}", tid=tid)
        recv_exact(conn, filesize)
        return

    # Buat subfolder per thread agar file tidak bentrok
    thread_dir = os.path.join(SAVE_DIR, f"client_{addr[0]}_{addr[1]}")
    os.makedirs(thread_dir, exist_ok=True)
    save_path = os.path.join(thread_dir, filename)

    received = 0
    with open(save_path, "wb") as f:
        while received < filesize:
            chunk = conn.recv(min(BUFFER, filesize - received))
            if not chunk:
                raise ConnectionError("Koneksi terputus saat menerima file.")
            f.write(chunk)
            received += len(chunk)
            pct = int(received / filesize * 30)
            bar = "█" * pct + "░" * (30 - pct)
            with print_lock:
                print(f"\r  [T-{tid:02d}] [{bar}] {received}/{filesize} byte", end="", flush=True)

    with print_lock:
        print()

    type_label = {
        "document": "DOKUMEN",
        "image":    "GAMBAR",
        "audio":    "AUDIO",
        "video":    "VIDEO",
    }.get(filetype, "FILE")

    tprint(f"{GREEN}[✓] TERIMA {type_label}: {filename} ({filesize:,} byte){RESET}", tid=tid)
    tprint(f"  └─ Disimpan ke: {save_path}", tid=tid)

# Func Thread Per Client
def client_handler(conn, addr, tid):
    """Dijalankan di thread terpisah untuk setiap client yang konek."""
    global active_threads

    with active_lock:
        active_threads += 1
        current = active_threads

    tprint(f"{CYAN}[+] Koneksi dari {addr[0]}:{addr[1]}  "
           f"(thread aktif: {current}){RESET}", tid=tid)

    try:
        with conn:
            while True:
                header = recv_header(conn)
                if header is None:
                    tprint(f"{YELLOW}[*] Client {addr[0]}:{addr[1]} selesai mengirim.{RESET}", tid=tid)
                    break

                dtype = header.get("type")
                if dtype == "text":
                    handle_text(conn, header, tid, addr)
                elif dtype == "file":
                    handle_file(conn, header, tid, addr)
                else:
                    tprint(f"{RED}[?] Tipe tidak dikenal: {dtype}{RESET}", tid=tid)

    except ConnectionError as e:
        tprint(f"{RED}[!] Koneksi error: {e}{RESET}", tid=tid)
    except Exception as e:
        tprint(f"{RED}[!] Error: {e}{RESET}", tid=tid)
    finally:
        with active_lock:
            active_threads -= 1
            remaining = active_threads
        tprint(f"{CYAN}[-] Koneksi {addr[0]}:{addr[1]} ditutup  "
               f"(thread aktif: {remaining}){RESET}", tid=tid)

# Main
def main():
    banner()
    os.makedirs(SAVE_DIR, exist_ok=True)

    tid_counter = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(10)  # antrian hingga 10 koneksi pending
        print(f"{YELLOW}[*] Menunggu koneksi (multi-thread) ...{RESET}\n")

        while True:
            conn, addr = srv.accept()
            tid_counter += 1
            t = threading.Thread(
                target=client_handler,
                args=(conn, addr, tid_counter),
                daemon=True,
                name=f"ClientThread-{tid_counter}"
            )
            t.start()
            with print_lock:
                print(f"{MAGENTA}[~] Thread-{tid_counter:02d} dimulai untuk {addr[0]}:{addr[1]}{RESET}")

main()
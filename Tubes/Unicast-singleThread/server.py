"""
UNICAST A -> B | SINGLE THREAD
Server Side
"""

import socket
import os
import struct
import json

# Config
HOST = '0.0.0.0'
PORT = 9090
BUFFER  = 4096 # 4KB
SAVE_DIR = "received_files"

# Extension yang diizinkan berdasarkan tipe
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
BOLD   = "\033[1m"
RESET  = "\033[0m"

def banner():
    print(f"""
{CYAN}{BOLD}
SERVER SIDE
{RESET}
Host : {HOST}   Port : {PORT}
Save : ./{SAVE_DIR}/
""")

# Helper: Terima data dengan panjang pasti
def recv_exact(conn, length):
    # Terima tepat `length` byte dari socket
    data = b""
    while len(data) < length:
        chunk = conn.recv(min(BUFFER, length - len(data)))
        if not chunk:
            raise ConnectionError("Koneksi terputus saat menerima data.")
        data += chunk
    return data

# Terima Header (Json)
def recv_header(conn):
    # Format header: [4 byte panjang header (big-endian)][JSON bytes]
    raw_len = recv_exact(conn, 4)
    hdr_len = struct.unpack(">I", raw_len)[0]
    hdr_bytes = recv_exact(conn, hdr_len)
    return json.loads(hdr_bytes.decode("utf-8"))

# Handler Per Tipe
def handle_text(conn, header):
    # Terima teks (kata / kalimat / paragraf)
    subtype = header.get("subtype", "text")
    length = header["length"]
    payload = recv_exact(conn, length)
    text = payload.decode("utf-8")

    label_map = {
        "words":     "KATA (1-5 kata)",
        "sentence":  "KALIMAT PANJANG",
        "paragraph": "PARAGRAF",
    }
    label = label_map.get(subtype, "TEKS")

    print(f"\n{GREEN}[✓] TERIMA {label}{RESET}")
    print(f"  └─ \"{text}\"")
    return True

def handle_file(conn, header):
    # Terima file (dokumen / gambar / audio / video)
    filename = header["filename"]
    filetype = header["filetype"]   # document / image / audio / video
    filesize = header["filesize"]
    ext = os.path.splitext(filename)[1].lower()

    # Validasi ekstensi
    allowed = ALLOWED_EXTENSIONS.get(filetype, [])
    if ext not in allowed:
        print(f"{RED}[✗] Ekstensi '{ext}' tidak diizinkan untuk tipe '{filetype}'{RESET}")
        # Tetap terima byte agar stream tidak rusak
        recv_exact(conn, filesize)
        return False

    # Simpan file
    os.makedirs(SAVE_DIR, exist_ok=True)
    save_path = os.path.join(SAVE_DIR, filename)

    received = 0
    with open(save_path, "wb") as f: # wb = write binary
        while received < filesize:
            chunk = conn.recv(min(BUFFER, filesize - received))
            if not chunk:
                raise ConnectionError("Koneksi terputus saat menerima file.")
            f.write(chunk)
            received += len(chunk)
            pct = int(received / filesize * 40)
            bar = "█" * pct + "░" * (40 - pct)
            print(f"\r  [{bar}] {received}/{filesize} byte", end="", flush=True)

    print()  # newline setelah progress bar

    type_label = {
        "document": "DOKUMEN",
        "image":    "GAMBAR",
        "audio":    "AUDIO",
        "video":    "VIDEO",
    }.get(filetype, "FILE")

    print(f"{GREEN}[✓] TERIMA {type_label}: {filename}{RESET}")
    print(f"  └─ Disimpan ke: {save_path}  ({filesize:,} byte)")
    return True

# Main
def main():
    banner()
    os.makedirs(SAVE_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        print(f"{YELLOW}[*] Menunggu koneksi dari Node A ...{RESET}\n")

        while True:
            conn, addr = srv.accept()
            with conn:
                print(f"{CYAN}[+] Koneksi diterima dari {addr[0]}:{addr[1]}{RESET}")
                try:
                    while True:
                        # Cek apakah masih ada data
                        raw_check = recv_exact(conn, 4)
                        hdr_len = struct.unpack(">I", raw_check)[0]

                        if hdr_len == 0:
                            # Sinyal selesai dari client
                            print(f"\n{YELLOW}[*] Client selesai mengirim.{RESET}\n")
                            break

                        hdr_bytes = recv_exact(conn, hdr_len)
                        header = json.loads(hdr_bytes.decode("utf-8"))
                        dtype = header.get("type")

                        if dtype == "text":
                            handle_text(conn, header)
                        elif dtype == "file":
                            handle_file(conn, header)
                        else:
                            print(f"{RED}[?] Tipe tidak dikenal: {dtype}{RESET}")

                except ConnectionError as e:
                    print(f"\n{RED}[!] Koneksi error: {e}{RESET}")
                except Exception as e:
                    print(f"\n{RED}[!] Error: {e}{RESET}")

                print(f"{CYAN}[-] Koneksi dari {addr[0]}:{addr[1]} ditutup.{RESET}\n")
                print(f"{YELLOW}[*] Menunggu koneksi baru ...{RESET}\n")

main()
# UNICAST A → B | MULTI THREAD
## Socket Programming — Tugas Besar

---

## Struktur File

```
unicast_multithread/
├── server_mt.py       ← Jalankan di Node B (penerima, multi-thread)
├── client_mt.py       ← Jalankan di Node A (pengirim, multi-thread)
└── received_files_mt/ ← Otomatis dibuat, subfolder per client
    ├── client_192.168.1.10_54321/
    │   ├── laporan.pdf
    │   └── foto.jpg
    └── client_192.168.1.11_54322/
        └── video.mp4
```

---

## Perbedaan dengan Single Thread

| Aspek | Single Thread | Multi Thread |
|-------|--------------|--------------|
| Koneksi server | 1 koneksi, sequential | Banyak koneksi paralel |
| Koneksi per sesi | 1 socket untuk semua | 1 socket baru per pengiriman |
| Konkurensi server | Tidak (blocking) | Ya (thread per client) |
| Konkurensi client | Tidak | Ya (menu 8: parallel send) |
| Output log | Normal | Label [T-XX] per thread |
| Simpan file | received_files/ | received_files_mt/client_IP_PORT/ |

---

## Cara Menjalankan

### Langkah 1 — Jalankan Server (Node B)
```bash
python server_mt.py
```

### Langkah 2 — Edit IP di client (jika beda mesin)
```python
SERVER_HOST = '127.0.0.1'   # ← ganti IP Node B
```

### Langkah 3 — Jalankan Client (Node A)
```bash
python client_mt.py
```

---

## Menu Pengiriman (Node A)

| Pilihan | Fungsi | Thread |
|---------|--------|--------|
| 1 | Kirim 1–5 Kata | 1 thread baru |
| 2 | Kirim Kalimat Panjang | 1 thread baru |
| 3 | Kirim Paragraf | 1 thread baru |
| 4 | Kirim Dokumen (.txt/.docx/.pdf) | 1 thread baru |
| 5 | Kirim Gambar (.jpg/.png) | 1 thread baru |
| 6 | Kirim Audio (.mp3) | 1 thread baru |
| 7 | Kirim Video (.mp4) | 1 thread baru |
| **8** | **Kirim SEMUA paralel** | **N thread sekaligus** |
| **9** | **Kirim SEMUA sequential** | **N thread, satu per satu** |
| 0 | Keluar | — |

---

## Arsitektur Thread

### Server (Node B)
```
main thread
   │
   ├── accept() → Thread-01 ─── handle client 192.168.1.10:54321
   ├── accept() → Thread-02 ─── handle client 192.168.1.10:54322
   ├── accept() → Thread-03 ─── handle client 192.168.1.11:54400
   └── ... (tidak terbatas)
```

### Client (Node A) — Menu 8 (parallel)
```
main thread
   │
   ├── Thread-01 ─── buka koneksi → kirim KATA      → tutup
   ├── Thread-02 ─── buka koneksi → kirim KALIMAT   → tutup
   ├── Thread-03 ─── buka koneksi → kirim PARAGRAF  → tutup
   ├── Thread-04 ─── buka koneksi → kirim DOKUMEN   → tutup
   ├── Thread-05 ─── buka koneksi → kirim GAMBAR    → tutup
   ├── Thread-06 ─── buka koneksi → kirim AUDIO     → tutup
   └── Thread-07 ─── buka koneksi → kirim VIDEO     → tutup
         (semua berjalan bersamaan)
```

---

## Protokol

Sama dengan single thread:
```
[4 byte: panjang header] [JSON header] [payload/file bytes]
[4 byte: 0x00000000]  ← sinyal selesai per koneksi
```

Perbedaan: setiap thread membuka **koneksi TCP tersendiri** ke server,
sehingga pengiriman dapat berjalan paralel tanpa blocking satu sama lain.

---

## Requirement

- Python 3.7+
- Tidak butuh library tambahan (built-in: `socket`, `threading`, `os`, `struct`, `json`)

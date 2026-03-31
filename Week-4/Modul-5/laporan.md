# Laporan Praktikum Jaringan Komputer IF - Week 4

## Pembahasan Modul 5

Pada modul 5 membahas mengenai UDP

### Pertanyaan beserta jawaban

1. Pilih satu paket UDP yang terdapat pada trace Anda. Dari paket tersebut, berapa banyak “field” yang terdapat pada header UDP? Sebutkan nama-nama field yang Anda temukan!<br>Ada 4, yaitu **Source Port, Destination Port, Length, dan Checksum.**

2. Perhatikan informasi “content field” pada paket yang Anda pilih di pertanyaan 1. Berapa panjang (dalam satuan byte) masing-masing “field” yang terdapat pada header UDP?<br>Setiap field pada header UDP memiliki panjang 2 byte, sehingga total panjang header UDP adalah 8 byte.

3. Nilai yang tertera pada ”Length” menyatakan nilai apa? Verfikasi jawaban Anda melalui paket UDP pada trace.<br>Length menunjukkan total panjang segmen UDP (header + data). Contoh: Length = 58 byte → 8 byte header + 50 byte payload.

4. Berapa jumlah maksimum byte yang dapat disertakan dalam payload UDP? (Petunjuk: jawaban untuk pertanyaan ini dapat ditentukan dari jawaban Anda untuk pertanyaan 2)<br>Jumlah max payload UDP adalah 65527 byte (65535 maksimum field Length – 8 byte header).

5. Berapa nomor port terbesar yang dapat menjadi port sumber? (Petunjuk: lihat petunjuk pada pertanyaan 4)<br>Nomor port terbesar yang dapat digunakan: 65535 (karena field port = 16 bit).

6. Berapa nomor protokol untuk UDP? Berikan jawaban Anda dalam notasi heksadesimal dan desimal. Untuk menjawab pertanyaan ini, Anda harus melihat ke bagian ”Protocol” pada datagram IP yang mengandung segmen UDP.<br>Nomor protokol: 17 (desimal) dan 0x11 (heksadesimal).

7. Periksa pasangan paket UDP di mana host Anda mengirimkan paket UDP pertama dan paket UDP kedua merupakan balasan dari paket UDP yang pertama. (Petunjuk: agar paket kedua merupakan balasan dari paket pertama, pengirim paket pertama harus menjadi tujuan dari paket kedua). Jelaskan hubungan antara nomor port pada kedua paket tersebut!<br>Hubungan port request–response:<br>- Request: Source Port = 4334, Destination Port = 161<br>- Response: Source Port = 161, Destination Port = 4334<br>- Menunjukkan pembalikan peran pengirim dan penerima.

### Bukti

Request:

![req](/Assets/img/Week-4/Modul-5/request.png)

Respond:

![respond](/Assets/img/Week-4/Modul-5/respond.png)
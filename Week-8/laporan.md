# Laporan Praktikum Jaringan Komputer IF - Week 6

## Tugas Modul 10

## IPv4

> Melakukan pelacakan route yang dilewati oleh komputer hingga sampai ke server `gaia.cs.umass.edu`

Langkah-langkah:

1. Pengecekan melalui command `tracert gaia.cs.umass.edu`

2. Gunakan filter Wireshark:

    - udp || icmp
    
    - ip.src==192.168.86.61 && ip.dst==128.119.245.12 && udp && !icmp
    
    - ip.dst==192.168.86.61 && icmp
    
Hasil:

- Paket UDP dikirim ke tujuan.

- Router perantara mengembalikan ICMP TTL-exceeded.

Bukti:

1. Command `tracert gaia.cs.umass.edu`
    
    ![cek IPv4](/Assets/img/Week-8/cek-ipv4.png)

    Dapat dilihat jika komputer melewati router (gateway) di 192.168.*** lalu menjuju ISP sebelum masuk ke jaringan internasional dan pada akhirnya sampai di server Umsass.

2. udp || icmp

    ![udp-icmp](/Assets/img/Week-8/udp-icmp.png)

3. ip.src==192.168.86.61 && ip.dst==128.119.245.12 && udp && !icmp

    ![ipsrc-ipdst-udp-!icmp](/Assets/img/Week-8/ip-icmp-udp.png)

4. ip.dst==192.168.86.61 && icmp

    ![ipdst-icmp](/Assets/img/Week-8/ip-icmp.png)

Kesimpulan: Traceroute memanfaatkan TTL dan ICMP untuk memetakan jalur hop ke tujuan.

> Menganalisis fragmentasi IP pada datagram UDP besar (±3000 byte).

Langkah-langkah:

1. Jalankan traceroute dengan ukuran 3000 byte.

2. Hilangkan filter, urutkan paket berdasarkan kolom Time.

3. Amati paket UDP besa.

4. Perhatikan fragmen IPv4 dengan Identification sama, Offset berbeda, dan MF flag.

Hasil:

1. Paket UDP besar (2972 byte) terfragmentasi.

2. Fragmen pertama: Offset = 0, MF = 1.

3. Fragmen kedua: Offset = 1480, MF = 0.

4. Semua fragmen punya Identification sama.

Bukti:

- UDP 3000:

    ![udp-3000](/Assets/img/Week-8/udp3K.png)

    Kesimpulan: Datagram UDP besar tidak dapat dikirim sekaligus sehingga IP memecahnya menjadi beberapa fragmen (fragmen dikenali melalui Identification, Offset, dan MF flag).

## IPv6

> Melihat sekilas datagram IPv6 dan DNS AAAA request.

Langkah-langkah:

1. Buka file ip-wireshark-trace2-1.pcapng.

2. Gunakan filter: frame.number < 300.

3. Amati paket ke-20 (t=3.814489).

Hasil:

1. Paket ke-20 adalah DNS AAAA request untuk youtube.com.

2. Header IPv6 menampilkan Traffic Class, Flow Label, Payload Length, Next Header, Hop Limit.

3. Alamat sumber dan tujuan berupa IPv6.

Bukti:

- IPv6

    ![ipv6](/Assets/img/Week-8/ipv6.png)

    Kesimpulan: IPv6 menggunakan DNS AAAA untuk resolusi nama ke alamat IPv6. Struktur header lebih sederhana dibanding IPv4.
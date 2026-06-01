# Laporan Praktikum Jaringan Komputer IF - Week 10

## Tugas Modul 10

> Menginvestigasi cara kerja protokol DHCP menggunakan Wireshark

## Penjelasan Tugas Modul 10

> Praktikum dilakukan menggunakan file trace DHCP dengan format .pcapng pada aplikasi Wireshark.

1. Release IP Address

    ![ipconfig-release](/Assets/img/Week-10/ipconfig-release.png)

    Command:
    ```cmd
    ipconfig /release
    ```

    Perintah `ipconfig /release` digunakan untuk melepaskan alamat IP yang sedang digunakan oleh device / computer. Setelah perintah dijalankan, komputer tidak lagi memiliki alamat IP dari DHCP server.

2. Renew IP Address

    ![ipconfig-renew](/Assets/img/Week-10/ipconfig-renew.png)

    Command:
    ```cmd
    ipconfig /renew
    ```

    Perintah `ipconfig /renew` digunakan untuk meminta alamat IP baru kepada DHCP server. Setelah proses berhasil, komputer akan memperoleh konfigurasi jaringan secara otomatis.

3. Filter Paket DHCP pada Wireshark

    ![Filter-DHCP](/Assets/img/Week-10/filter-dhcp.png)

    Filter `dhcp` digunakan untuk menampilkan hanya paket DHCP pada Wireshark. Paket yang muncul:
    - DHCP Discover
    - DHCP Offer
    - DHCP Request
    - DHCP ACK

4. DHCP Discover

    ![DHCP-discover](/Assets/img/Week-10/discover.png)

    DHCP Discover adalah paket pertama yang dikirim oleh client untuk mencari DHCP server yang tersedia pada jaringan.

5. DHCP Offer

    ![DHCP-offer](/Assets/img/Week-10/offer.png)

    DHCP Offer merupakan paket balasan dari DHCP server yang berisi penawaran alamat IP kepada client. Informasi yang diberikan:
    - Alamat IP
    - Subnet mask
    - Gateway
    - Lease time

6. DHCP Request

    ![DHCP-request](/Assets/img/Week-10/request.png)

    DHCP Request dikirim oleh client untuk meminta penggunaan alamat IP yang telah ditawarkan oleh DHCP server (untuk mengkonfirmasi pilihan alamat IP dan memberitahu server bahwa client menerima penawaran IP).

7. DHCP ACK

    ![DHCP-ack](/Assets/img/Week-10/ack.png)

    DHCP ACK merupakan balasan akhir dari DHCP server yang menyatakan bahwa alamat IP telah resmi diberikan kepada client.

## Urutan Proses DHCP

> Terdiri dari empat tahap utama:

1. Discover Client: mencari DHCP server

2. Offer Server: menawarkan alamat IP

3. Request Client: meminta alamat IP yang ditawarkan

4. ACK Server: menyetujui dan memberikan alamat IP
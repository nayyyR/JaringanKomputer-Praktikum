# Laporan Praktikum Jaringan Komputer IF - Week 4

## Pembahasan Modul 4

> Berikut adalah hal yang dibahas pada praktikum jaringan komputer modul 4

1. [Nslookup](#nslookup)
2. [Ipconfig](#ipconfig)
3. [Tracing DNS dengan Wireshark](#tracing-dns-dengan-wireshark)

## Nslookup

> Nslookup memungkinkan host yang menjalankan perintah untuk bertanya mengenai suatu server DNS dan mendapatkan informasi DNS dari server tersebut.

![nslookup](/Assets/img/Week-4/Modul-4/nslookup.jpeg)

Penjelasan command nslookup:

1. **nslookup www.facebook.com**<br><div align="justify">Pada command ini, saat menjalankan nslookup tanpa menentukan server DNS yang diinginkan, maka nslookup mengirimkan permintaan ke default server DNS lokal. Dengan kata lain command ini berarti "tolong kirimkan alamat IP untuk host www.facebook.com".</div><br>Informasi yang diberikan adalah:<br>i. Nama dan alamat IP server DNS yang memberikan jawaban dari perintah yang dimasukkan.<br>ii. Jawaban dari perintah tersebut, berupa nama host dan alamat IP www.facebook.com.

2. **nslookup -type=NS facebook.com**<br><div align="justify">Pada command ini, opsi `-type=NS` menyebabkan nslookup mengirimkan permintaan untuk record tipe-NS ke default server DNS lokal. Dengan kata lain, permintaan tersebut berarti, "tolong kirimkan saya nama host dari DNS otoritatif untuk facebook.com".(Tpe NS untuk menanyakan Name Server yang berwenang atas sebuah domain)</div><br>Hasil yang diberikan adalah:<br>Server DNS yang memberikan jawaban (yang merupakan default server DNS lokal) serta 4 nama server facebook. Keempat server tersebut merupakan server DNS otoritatif untuk host facebook.

3. **nslookup www.facebook.com 8.8.8.8**<br><div align="justify">Pada command ini, saat menjalankan nslookup dengan menentukan server DNS yang diinginkan, maka nslookup mengirimkan permintaan ke DNS yang telah ditentukan.</div><br>Informasi yang diberikan adalah:<br>i. Nama dan alamat IP server DNS yang telah ditentukan.<br>ii. Jawaban dari perintah tersebut, berupa nama host dan alamat IP www.facebook.com.

### Pertanyaan beserta jawaban mengenai nslookup:

1. Jalankan nslookup untuk mendapatkan alamat IP dari server web di Asia. Berapa alamat IP server tersebut?<br>Pada percobaan ini, saya menggunakan web www.facebook.com dengan ip yang didapatkan adalah 157.240.15.35

2. Jalankan nslookup agar dapat mengetahui server DNS otoritatif untuk universitas di Eropa.<br>Pada percobaan ini, saya mencoba untuk melakukan pengecekan DNS dari Universitas Oxford. Berikut adalah hasilnya:<br>![web-univ-europe](/Assets/img/Week-4/Modul-4/nslookup-europe.png)

3. Jalankan nslookup untuk mencari tahu informasi mengenai server email dari Yahoo! Mail melalui salah satu server yang didapatkan di pertanyaan nomor 2. Apa alamat IP-nya?<br>![yahoo-europe](/Assets/img/Week-4/Modul-4/informasi-yahoo-europe.png)<br>Pada percobaan ini DNS otoritatif yang hanya melayani domain `ox.ac.uk` dan tidak mengizinkan query untuk domain eksternal seperti `yahoo.com`. Sehingga diperoleh hasil query refused. Untuk alamat ipnya sendiri adalah 129.67.1.190 untuk `dns0.ox.ac.uk` dan 129.67.1.191 untuk `dns1.ox.ac.uk`. (type=MX berfungsi untuk mencari mail exchange record dari suatu domain)

## Ipconfig

> Ipconfig dapat digunakan untuk menampilkan informasi mengenai TCP/IP client saat ini, termasuk alamat IP alamat server DNS, jenis adaptor, dan sebagainya.

Command ipconfig:

1. **ipconfig /all**<br>![ipconfig-all](/Assets/img/Week-4/Modul-4/ipconfig-all.png)<br><div align="justify">Command ini digunakan untuk menampilkan detail lengkap termasuk MAC address, DHCP server, dan DNS server untuk semua adaptor.</div>

2. **ipconfig /displaydns**<br>![ipconfig-displaydns](/Assets/img/Week-4/Modul-4/ipconfig-displaydns.png)<br><div align="justify">Command ini digunakan untuk menampilkan daftar isi cache resolver DNS yang tersimpan di komputer Windows, termasuk nama host, alamat IP, dan Time to Live (TTL) dari situs web yang baru saja diakses.</div>

3. **ipconfig /flushdns**<br>![ipconfig-flushdns](/Assets/img/Week-4/Modul-4/ipconfig-flushdns.png)<br><div align="justify">Command ini digunakan untuk mengosongkan catatan DNS berarti menghapus semua record dan memuat ulang record dari file host. </div>

## Tracing DNS dengan Wireshark

1. Gunakan ipconfig untuk mengosongkan catatan DNS di host.<br>![ipconfig-flushdns](/Assets/img/Week-4/Modul-4/ipconfig-flushdns.png)

2. Buka browser dan kosongkan cache-nya.<br>![kosongkan-cache-browser](/Assets/img/Week-4/Modul-4/clear-cache-browser.png)

3. Buka Wireshark dan masukkan "ip.addr == <your_IP_address> && DNS" ke dalam filter. Bagian <your_IP_address> diisi dengan alamat IP kita yang didapatkan melalui ipconfig. Filter ini akan menghapus semua paket yang tidak berasal atau ditujukan ke host.<br>![filter-ip](/Assets/img/Week-4/Modul-4/filter-ip-dns.png)

4. Mulai pengambilan paket di Wireshark. 

5. Dengan browser Anda, kunjungi halaman web: http://www.ietf.org<br>![open-url](/Assets/img/Week-4/Modul-4/web-ietf.png)

6. Hentikan pengambilan paket.<br>![wireshark-result](/Assets/img/Week-4/Modul-4/filter-ip-dns-result.png)

### Pertanyaan beserta jawaban mengenai tracing dns:

1. Cari pesan permintaan DNS dan balasannya. Apakah pesan tersebut dikirimkan melalui UDP atau TCP?<br>Pesan yang saya gunakan adalah `AAAA www.ietf.org` dan pesan tersebut dikirimkan melalui UDP.<br>![udp-proof](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no1.png)

2. Apa port tujuan pada pesan permintaan DNS? Apa port sumber pada pesan balasannya?<br>Pada pesan permintaan `AAAA www.ietf.org` port tujuannya adalah 53 sedangkan pada pesan balasannya adalah 49173.<br>Request:<br>![req](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no2-req.png)<br>Respone:<br>![respone](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no2-respone.png)

3. Pada pesan permintaan DNS, apa alamat IP tujuannya? Apa alamat IP server DNS lokal anda (gunakan ipconfig untuk mencari tahu)? Apakah kedua alamat IP tersebut sama?<br>Ip tujuan dari pesan req:<br>![ip-tujuan](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no3-ip-tujuan.png)<br>DNS local:<br>![dns-local](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no3-dns.png)<br>Alamat tujuan dari pesan req sama dengan dns local punya saya.

4. Periksa pesan permintaan DNS. Apa “jenis" atau ”type” dari pesan tersebut? Apakah pesan permintaan tersebut mengandung ”jawaban” atau ”answers”?<br>![type-answer](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no4.png)<br>Pada pesan req, typenya adalah `AAAA` dan untuk answers sendiri berisi `0` yang berarti tidak ada jawaban.

5. Periksa pesan balasan DNS. Berapa banyak ”jawaban” atau ”answers” yang terdapat di dalamnya? Apa saja isi yang terkandung dalam setiap jawaban tersebut?<br>![respone-answers](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no5.png)<br>Ada 2 jawaban dari pesan balasan.

6. Perhatikan paket TCP SYN yang selanjutnya dikirimkan oleh host Anda. Apakah alamat IP pada paket tersebut sesuai dengan alamat IP yang tertera pada pesan balasan DNS?<br>![tcp-syn](/Assets/img/Week-4/Modul-4/Pertanyaan-Tracing/tracing-no6.png)<br>Dapat dilihat kalau source dan destination alamat IP antar paket saling berkebalikan yang berarti mereka success dalam berkomunikasi.

7. Halaman web yang sebelumnya anda akses (http://www.ietf.org) memuat beberapa gambar. Apakah host Anda perlu mengirimkan pesan permintaan DNS baru setiap kali ingin mengakses suatu gambar?<br> Tidak perlu.

### Pertanyaan beserta jawaban menganai tracing x nslookup:

> Menggunakan nslookup www.mit.edu

Running:

![cmd-nslookup](/Assets/img/Week-4/Modul-4/Nslookup-2/nslookup2-no1-cmd.jpeg)

![wireshark-nslookup](/Assets/img/Week-4/Modul-4/Nslookup-2/nslookup2-no1-wireshark.jpeg)

Pertanyaan dan jawaban:

1. Apa port tujuan pada pesan permintaan DNS? Apa port sumber pada pesan balasan DNS?<br>Pada request, port tujuannya adalah `53` sedangkan pada respone, source portnya adalah `53`.

2. Ke alamat IP manakah pesan permintaan DNS dikirimkan? Apakah alamat IP tersebut merupakan default alamat IP server DNS lokal Anda?<br>Pada request, tujuan alamat IP nya adalah `8.8.8.8` dan bukan merupakan IP default DNS lokal saya melainkan IP dari DNS google.

3. Periksa pesan permintaan DNS. Apa ”jenis” atau ”type” dari pesan tersebut? Apakah pesan tersebut mengandung ”jawaban” atau ”answers”?<br>Pada request, typenya adalah `A`. Sedangkan untuk answers pada request adalah `0` yang berarti tidak ada jawaban.

4. Periksa pesan balasan DNS. Berapa banyak ”jawaban” atau “answers” yang terdapat di dalamnya. Apa saja isi yang terkandung dalam setiap jawaban tersebut?<br>Ada 3 answers yang diberikan, yaitu:<br>i. www.mit.edu: type CNAME, class IN, cname www.mit.edu.edgekey.net => Artinya: www.mit.edu adalah alias yang diarahkan ke domain lain.<br>ii. www.mit.edu.edgekey.net: type CNAME, class IN, cname e9566.dscb.akamaiedge.net => Artinya: domain tersebut masih alias lagi ke domain berikutnya.<br>iii.e9566.dscb.akamaiedge.net: type A, class IN, addr 23.217.163.122 => Artinya: domain ini sudah menunjuk ke alamat IP asli (tujuan akhir).

<br>

> Menggunakan nslookup -type=NS mit.edu

Running:

![cmd-type](/Assets/img/Week-4/Modul-4/Nslookup-2/nslookup2-no2.jpeg)

Pertanyaan dan jawaban:

1. Ke alamat IP manakah pesan permintaan DNS dikirimkan? Apakah alamat IP tersebut merupakan default alamat IP server DNS lokal Anda?<br>Dikirimkan ke `8.8.8.8` yang merupakan dns google dan bukan merupakan alamat IP DNS lokal saya.

2. Periksa pesan permintaan DNS. Apa ”jenis” atau ”type” dari pesan tersebut? Apakah pesan tersebut mengandung ”jawaban” atau ”answers”?<br>Type: NS dan request tidak mengandung answers.

3. Periksa pesan balasan DNS. Apa nama server MIT yang diberikan oleh pesan balasan? Apakah pesan balasan ini juga memberikan alamat IP untuk server MIT tersebut?<br>Isi balasan sebagai berikut ini:<br><br>Nama server MIT:<br>- ns1-173.akam.net<br>- asia2.akam.net<br>- asia1.akam.net<br>- ns1-37.akam.net<br>- usw2.akam.net<br>- use5.akam.net<br>- use2.akam.net<br>- eur5.akam.net<br><br>Alamat IP beberapa server MIT(Ipv4):<br>- eur5.akam.net → 23.74.25.64<br>- use5.akam.net → 2.16.40.64<br>- asia1.akam.net → 95.100.175.64<br>- ns1-37.akam.net → 193.108.91.37<br><br>Alamat IP beberapa server MIT(Ipv6):<br>- use5.akam.net → 2600:1403:a::40<br>- ns1-37.akam.net → 2600:1401:2::25

<br>

> Menggunakan nslookup www.aiit.or.kr bitsy.mit.edu

Running:

![cmd-bitsy](/Assets/img/Week-4/Modul-4/Nslookup-2/nslookup2-no3.jpeg)

Pertanyaan dan jawaban:

1. Ke alamat IP manakah pesan permintaan DNS dikirimkan? Apakah alamat IP tersebut merupakan default alamat IP server DNS lokal Anda?<br>Dikirimkan ke `bitsy.mit.edu → 18.0.72.3` dan bukan merupakan alamat IP DNS lokal saya.

2. Periksa pesan permintaan DNS. Apa ”jenis” atau ”type” dari pesan tersebut? Apakah pesan tersebut mengandung ”jawaban” atau ”answers”?<br>Type: A dan mengandung answers.

3. Periksa pesan balasan DNS. Berapa banyak ”jawaban” atau “answers” yang terdapat di dalamnya. Apa saja isi yang terkandung dalam setiap jawaban tersebut?<br>Isi balasannya adalah alamat IP untuk www.aiit.or.kr:<br>- 2606:4700:3031::ac43:9878<br>- 2606:4700:3036::6815:4a08<br>- 172.67.152.120<br>- 104.21.74.8
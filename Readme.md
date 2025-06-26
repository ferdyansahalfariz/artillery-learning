# Template Artillery Untuk Performance Test Hasura DDN

referensi: https://github.com/hasura/postsales/tree/main/Tools/hasura-test-suite/DDN

Kali ini saya menggunakan hasura DDN cloud sebagai service graphql nya, jadi diperlukan penyesuaian seperti header dan lain sebagainya jika ingin menggunakannya untuk hasura DDN On-Prem ataupun hasura V2

## Pre-req
1. Install Artillery

https://www.artillery.io/docs/get-started/get-artillery

Pada dokumentasi ini digunakan versi artillery : 

- Artillery: 2.0.23

- Node.js:   v22.16.0

2. Python 

Hal ini digunakan untuk running script `generate-report.py` saat ingin membuat report HTML dari file output json setelah melakukan running Artillery 

Dalam dokumentasi ini digunakan versi Python:

- Python 3.11.10

## Cara Running

1. Sesuaikan terlebih dahulu GRAPHQL_HOST dan DDN_TOKEN dengan value yang benar pada file `.env`

2. sesuaikan juga beberapa isian dalam file yaml `artillery-graphql-tester.yaml` sebagai file yang akan di input untuk run Artillery nya.

Adapun penyesuaian yang bisa dilakukan yaitu:

- `phases` yang berisi durasi, arrival rate, ramp to dan name 
- `scenarios` yang berisi query yang di hit, maupun pengaturan custom lainnya

3. run file yaml dengan command :

```
npx artillery run artillery-graphql-tester.yaml -o results-json/output-artillery-graphql-test.json --env-file .env
```
command itu akan menginput file yaml `artillery-graphql-tester.yaml` dengan berdasarkan pada file env `.env` sebagai env var nya kemudian hasil running artillerynya akan disimpan ke file json `results-json/output-artillery-graphql-test.json`

## Generate report dari output json file ke HTML

File output json kemudian bisa di generate menjadi file HTML dari custom script `scripts/generate_report.py` agar hasil yang di dapat menjadi lebih informatif karena sudah di visualisasikan. Berikut command untuk generate nya:

```
python3 scripts/generate_report.py results-json/output-artillery-graphql-test.json
```

Berikut adalah contoh hasil generate file HTML nya saat dibuka di browser:


![image](https://github.com/user-attachments/assets/2437a72b-1713-426b-b40f-1a73bb31b8c1)


![image](https://github.com/user-attachments/assets/94c5f38e-bf22-4f77-a12e-962bf3cdb0ec)


![image](https://github.com/user-attachments/assets/e2adaf75-159a-4425-af2a-1141b706f6b2)


![image](https://github.com/user-attachments/assets/561090dd-3e01-4819-b95d-758ab56c9fb8)


# 🔍 Perbandingan JMeter vs Artillery

Referensi: https://azevedorafaela.com/2020/06/09/load-tests-jmeter-vs-artillery/

## Tabel Perbandingan

| Aspek | **JMeter** | **Artillery** |
|-------|------------|---------------|
| **Dukungan Protokol** | HTTP, FTP, JDBC, SOAP, LDAP, TCP, JMS, SMTP, POP3, IMAP | HTTP, WebSocket, Socket.io |
| **Penulisan Skrip** | GUI oriented | script-oriented |
| **Pendekatan "Test as Code"** | Lemah, sulit digunakan, berbasis Java | Kuat, berbasis YAML/JSON, mudah dipelihara |
| **Fleksibilitas Ramp-Up** | Butuh plugin untuk fleksibilitas | Native support ramp-up dan fase beban fleksibel |
| **Analisis Hasil Tes** | Ada, melalui GUI dan listener | Ada, melalui report akhir atau log terminal |
| **Konsumsi Resource** | Berat, konsumsi memori tinggi saat banyak pengguna | Ringan, efisien, mendukung multicore |
| **Integrasi dengan Version Control (Git, dll.)** | Sulit (karena berbasis GUI) | Mudah (karena berbasis file/script) |
| **Jumlah Pengguna Bersamaan** | Ribuan (dengan batasan & konfigurasi tambahan) | Ribuan pengguna lebih ringan di satu mesin |
| **Fitur Perekaman Skrip (Script Recording)** | Ada | Tidak tersedia |
| **Eksekusi Terdistribusi** | Ya | Ya |
| **Monitoring Saat Tes** | Ada, tapi konsumsi memori tinggi | Tidak realtime, hanya laporan akhir atau log terminal |

---

## ✅ Kelebihan Artillery dibanding JMeter

- **Ringan dan Cepat**  
  Lebih ringan dijalankan di mesin lokal, bahkan untuk ribuan pengguna. Konsumsi resource rendah dan efisien.

- **Mudah Dipelihara**  
  Skrip berbasis YAML/JSON mudah dibaca, ditulis, dan diintegrasikan ke version control.

- **Modern dan Fleksibel**  
  Native support untuk WebSocket dan Socket.io. Tidak butuh GUI.

- **Cepat dalam Penulisan Skrip**  
  Tersedia mode cepat, tidak butuh pembuatan skrip kompleks.

- **Mudah Diintegrasikan**  
  Mudah diinstal (berbasis Node.js), cocok untuk CI/CD pipeline.

---

## ❌ Kekurangan Artillery dibanding JMeter

- **Dukungan Protokol Terbatas**  
  Tidak cocok jika membutuhkan FTP, SOAP, JDBC, atau protokol lainnya.

- **Tidak Ada Fitur Perekaman**  
  Tidak tersedia script recording seperti di JMeter.

- **Monitoring Terbatas**  
  Tidak mendukung monitoring real-time.

- **Kurang Ideal untuk Tes Kompleks**  
  Tidak cocok untuk skenario load test yang kompleks dengan banyak protokol atau integrasi berat.

## Kapan Sebaiknya Memilih Artillery?
- Jika butuh tool ringan, cepat, dan cocok untuk CI/CD.

- Skenario test tidak terlalu kompleks dan berbasis HTTP/WebSocket.

- Jika menginginkan tes berbasis file/script, bukan GUI.

- Infrastruktur berbasis Node.js dan container-friendly.

## Kapan Sebaiknya Memilih JMeter?
- Jika butuh dukungan berbagai protokol (FTP, JDBC, SOAP, dll.).

- Perlu GUI untuk membuat/melihat skenario dengan drag & drop.

- Butuh recording untuk mempercepat penulisan skrip.

- Infrastruktur sudah biasa dengan Java-based tools dan legacy systems.
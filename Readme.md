# Template Artillery Untuk Performance Test Hasura DDN

referensi: https://github.com/hasura/postsales/tree/main/Tools/hasura-test-suite/DDN

Kali ini saya menggunakan hasura DDN cloud sebagai service graphql nya, jadi diperlukan penyesuaian seperti header dan lain sebagainya jika ingin menggunakannya untuk hasura DDN On-Prem ataupun hasura V2

## Pre-req
1. Install Artillery

https://www.artillery.io/docs/get-started/get-artillery

Pada dokumentasi ini digunakan versi artillery : 

Artillery: 2.0.23

Node.js:   v22.16.0

2. Python 

Hal ini digunakan untuk running script `generate-report.py` saat ingin membuat report HTML dari file output json setelah melakukan running Artillery 

Dalam dokumentasi ini digunakan versi Python:

3.11.10

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

4. File output json kemudian bisa di generate menjadi file HTML dari custom script `scripts/generate_report.py` agar hasil yang di dapat menjadi lebih informatif karena sudah di visualisasikan. berikut adalah contoh hasil generate file HTML nya saat dibuka di browser:


![image](https://github.com/user-attachments/assets/2437a72b-1713-426b-b40f-1a73bb31b8c1)


![image](https://github.com/user-attachments/assets/94c5f38e-bf22-4f77-a12e-962bf3cdb0ec)


![image](https://github.com/user-attachments/assets/e2adaf75-159a-4425-af2a-1141b706f6b2)


![image](https://github.com/user-attachments/assets/561090dd-3e01-4819-b95d-758ab56c9fb8)

# Smartren postgresql function parser (and ETL)

## Deskripsi

Parser fungsi postgresql untuk mengambil metadata dependensi tabel.

## *Quick Start*

### 0. Prerequisities

Pastikan python memiliki versi `3.6` atau lebih dengan menjalankan perintah berikut:

```bash
python3 --version
# Python 3.6.9
```
Jika perintah `python3` gagal atau memiliki versi yang lebih rendah, silahkan pasang terlebih dahulu minimal versi **3.6**.

Pastikan `git` telah terpasang dengan menjalankan perintah berikut:
```bash
git --version
# git version 2.17.1
```
Jika perintah `git` gagal, silahkan pasang terlebih dahulu.

### 1. Clone repository dengan `git`

Jalankan perintah berikut untuk menyalin *source code* dengan `git`:

```bash
git clone https://github.com/rochimfn/pgsql-parser-func.git
```
### 2. Masuk ke direktori

```
cd pgsql-parser-func
```

### 3. Memasang dependensi

**WARNING:** Perintah berikut akan memasang library secara **global**.

Tidak disarankan untuk production!
```
pip install -r requirements.txt
```

### 4. Mengatur kredensial pada `settings.py`

Sesuaikan kredensial pada berkas `settings.py`

Contoh:

```python
sqlite_db = 'data/function.db'

psql_host = '127.0.0.1'
psql_username = 'admin'
psql_password = 'password'
psql_db = 'dev'
psql_schema = 'public'
psql_table = 'hasil_parsing'

neo4j_driver = 'neo4j'
neo4j_host = 'localhost'
neo4j_username = 'neo4j'
neo4j_password = 'password'

```

### 5. Menjalankan `pull.py`

```bash
python3 pull.py
```

### 6. Menjalankan `main.py`

```bash
python3 main.py db data/function.db persist
```

### 7. Menjalankan `push.py`

```bash
python3 push.py
```

### 8. Membaca dokumentasi

Section `quick start` ditujukan hanya untuk memulai dengan cepat. Penggunaan untuk produksi diharuskan memperhatikan setiap bagian dalam dokumentasi berikut.

## Pemasangan Dependensi

Script ini hanya mendukung python versi 3.

### Menggunakan Virtual Environments

Buat dahulu virtual environmentsnya

```bash
python3 -m venv venv
# atau
virtualenv3 venv
# atau
python3 -m virtualenv venv
```

Masuk ke virtual environments

```bash
source venv/bin/activate # pada *Nix os
venv\Scripts\activate # pada Windows
```

Memasang dependensi dengan `pip`

```bash
pip install -r requirements.txt
```

Keluar dari virtual environments

```bash
deactivate
```

### Tanpa Menggunakan Virtual Enviroments

Pasang dependensi dengan `pip3`.

```bash
pip3 install -r requirements.txt
```

## Konfigurasi

Jalankan perintah git berikut untuk mengecualikan `settings.py` dan `get_function.sql` dari git index. Hal ini __WAJIB__ dilakukan untuk menghindari kredensial ikut tercatat oleh version control system (git).

```bash
git update-index --assume-unchanged settings.py
git update-index --assume-unchanged get_function.sql #jika ingin mengganti kueri pengambil function
```

Atur kredensial pada berkas `settings.py`

Contoh:

```python
sqlite_db = 'data/function.db'

psql_host = '127.0.0.1'
psql_username = 'admin'
psql_password = 'password'
psql_db = 'dev'
psql_schema = 'public'
psql_table = 'hasil_parsing'

neo4j_driver = 'neo4j'
neo4j_host = 'localhost'
neo4j_username = 'neo4j'
neo4j_password = 'password'

```

## Menjalankan

Terdapat 3 script yaitu `main.py`, `push.py` dan `pull.py`. Berikut merupakan fungsinya:
* `main.py` merupakan script utama yang berfungsi membaca postgresql function dan mengembalikan metadata terkait tabel.
* `pull.py` merupakan script bantuan yang berfungsi mengambil definisi fungsi dari `INFORMATION_SCHEMA` lalu menyimpannya dalam database sqlite lokal.
* `push.py` merupakan script bantuan yang berfungsi membaca luaran dari fungsi utama lalu mentransformasi kedalam bentuk graph di database neo4j. 

### Menjalankan `main.py`

Sebelum menjalankan, pastikan semua dependensi telah terpasang. Pastikan virtual environments telah aktif (jika menggunakan).

`main.py` membutuhkan 2 argumen wajib `source` dan `path` dan 1 argumen opsional `persist`. Argumen `source` memilki nilai `db` atau `file`. Sedangkan argumen `path` dapat berisi path yang menunjukkan lokasi berkas. Argumen opsional `persist` dapat digunakan jika ingin menyimpan hasil parsing ke database.

* `source` (db/file)
    * `db`: script akan membaca definisi fungsi dari berkas database sqlite3. Secara default, script `pull` akan menyimpan definisi fungsi ke database sqlite di `data/function.db`.
    * `file`: script akan membaca definisi fungsi dari berkas teks.
* `path` (path/to/file)
* `persist`

Contoh:

```bash
python main.py file data/function.sql persist
python main.py db data/function.db persist
```

Jika eksekusi sukses, script akan menyimpannya hasil parsing ke berkas `output/text.csv`. Berkas `text.csv` adalah berkas csv dengan delimiter titik koma (';') tanpa header. Script juga akan menampilkan hasil parsing ke konsol.

### Menjalankan `pull.py`

Sebelum menjalankan, pastikan semua dependensi telah terpasang. Pastikan virtual environments telah aktif (jika menggunakan).

Script ini mengharuskan konfigurasi sqlite(_sqlite_\_) dan postgresql (_psql_\_) pada `settings.py` untuk diatur terlebih dahulu.

Script `pull.py` tidak membutuhkan argumen, untuk menjalankan gunakan perintah berikut:

```bash
python pull.py
```

Jika eksekusi berhasil, script akan mengembalikan `Done` pada konsol. Secara default, definisi fungsi akan disimpan pada database sqlite di `data/function.db`.

### Menjalankan `push.py`

Sebelum menjalankan, pastikan semua dependensi telah terpasang. Pastikan virtual environments telah aktif (jika menggunakan).

Script ini mengharuskan konfigurasi neo4j (_neo4j_\_) pada `settings.py` untuk diatur terlebih dahulu.

Script `push.py` tidak membutuhkan argumen, namun memerlukan berkas `output/text.csv` sebagai sumber data (secara default, script `main.py` akan menghasilkan berkas ini). Untuk menjalankan script gunakan perintah berikut:

```bash
python push.py
```

Jika eksekusi berhasil, relasi antar fungsi dan tabel akan tersimpan pada database neo4j.

## Troubleshooting

### Error: gcc executable not found
* Solusi:
    * ubuntu: pasang `build-essential`
    * centos: pasang `gcc gcc-c++ make `


### Error: pg_config executable not found
* Referensi: https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
* Solusi: 
	* ubuntu: pasang `libpq-dev`
	* centos: pasang `libpq-devel`

### psycopg: Python.h: No such file or directory
* Referensi https://stackoverflow.com/questions/19843945/psycopg-python-h-no-such-file-or-directory
* Solusi:
	* pasang python versi dev `python3-dev` atau `python3-devel`

### Error lain
* Solusi:
    * [Google](https://www.google.com)
    * Buat [tiket](https://github.com/rochimfn/pgsql-parser-func/issues/new)
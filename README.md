# Sistem Pakar Diagnosis Printer

Sistem pakar berbasis pengetahuan untuk mendiagnosis kerusakan printer menggunakan dua metode penalaran: **Rule-Based Reasoning (RBR)** dan **Case-Based Reasoning (CBR)**. Aplikasi ini dibangun menggunakan Python dan Streamlit, dengan antarmuka web yang interaktif dan intuitif.

---

## Daftar Isi

1. [Gambaran Umum](#gambaran-umum)
2. [Fitur Utama](#fitur-utama)
3. [Arsitektur Sistem](#arsitektur-sistem)
4. [Struktur Direktori](#struktur-direktori)
5. [Prasyarat](#prasyarat)
6. [Instalasi](#instalasi)
7. [Menjalankan Aplikasi](#menjalankan-aplikasi)
8. [Panduan Penggunaan](#panduan-penggunaan)
9. [Metode Rule-Based Reasoning (RBR)](#metode-rule-based-reasoning-rbr)
10. [Metode Case-Based Reasoning (CBR)](#metode-case-based-reasoning-cbr)
11. [Knowledge Base](#knowledge-base)
12. [Case Library](#case-library)
13. [Referensi](#referensi)

---

## Gambaran Umum

Sistem ini memanfaatkan dua pendekatan dalam bidang kecerdasan buatan untuk mendiagnosis kerusakan printer:

- **Rule-Based Reasoning (RBR)**: Menggunakan metode Forward Chaining dengan aturan IF-THEN yang didefinisikan oleh pakar. Cocok untuk kasus-kasus yang memiliki pola gejala yang jelas dan sudah terdokumentasi.

- **Case-Based Reasoning (CBR)**: Menggunakan siklus Retrieve-Reuse-Revise-Retain untuk mencari solusi berdasarkan kasus-kasus serupa yang pernah ditangani sebelumnya. Cocok untuk kasus-kasus baru yang belum memiliki aturan eksplisit.

Kedua metode saling melengkapi: RBR memberikan diagnosis deterministik berdasarkan aturan yang sudah pasti, sedangkan CBR memberikan fleksibilitas untuk menangani kasus-kasus baru berdasarkan pengalaman masa lalu.

---

## Fitur Utama

### Diagnosis RBR (Rule-Based Reasoning)
- Forward Chaining dengan AND logic
- Pertanyaan gejala satu per satu (step-by-step)
- Exact match dan partial match
- Inference trace (jejak penalaran) untuk transparansi proses
- Navigasi maju dan mundur antar pertanyaan

### Diagnosis CBR (Case-Based Reasoning)
- Siklus lengkap Retrieve-Reuse-Revise-Retain
- Weighted Nearest Neighbor untuk perhitungan similarity
- Similarity breakdown per gejala (transparansi perhitungan)
- Formulir untuk menyimpan kasus baru ke case library
- Referensi URL yang dapat diklik untuk setiap kasus

### Basis Pengetahuan
- 9 gejala kerusakan printer dengan bobot dan kategori
- 5 aturan diagnosis (IF-THEN rules)
- Referensi URL terverifikasi untuk setiap aturan

### Case Library
- 32 kasus diagnosis printer dari berbagai merek
- Setiap kasus memiliki referensi URL yang terverifikasi
- Filter berdasarkan merek dan tingkat keparahan
- Statistik case library

### Antarmuka Pengguna
- Desain dark theme modern dengan gradient dan animasi
- Sidebar navigasi yang intuitif
- Dashboard beranda dengan metrik ringkasan
- Responsive layout

---

## Arsitektur Sistem

```
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|   Knowledge Base  |     |   Case Library    |     |   UI Layer        |
|   (JSON)          |     |   (JSON)          |     |   (Streamlit)     |
|                   |     |                   |     |                   |
+--------+----------+     +--------+----------+     +--------+----------+
         |                         |                          |
         v                         v                          v
+--------+----------+     +--------+----------+     +--------+----------+
|                   |     |                   |     |                   |
|   KnowledgeBase   |     |   CBR Engine      |     |   app.py          |
|   (Python Class)  |     |   (Python Class)  |     |   (Router &       |
|                   |     |                   |     |    Page Renderer) |
+--------+----------+     +-------------------+     +-------------------+
         |
         v
+--------+----------+
|                   |
|   RBR Engine      |
|   (Python Class)  |
|                   |
+-------------------+
```

### Alur Diagnosis

```
User Input (Gejala)
    |
    +---> RBR Engine ---> Forward Chaining ---> Rule Matching ---> Diagnosis
    |
    +---> CBR Engine ---> Retrieve (Similarity) ---> Reuse ---> Revise ---> Retain
```

---

## Struktur Direktori

```
printer-diagnosis-expert-system/
|
|-- app.py                          # Aplikasi utama Streamlit
|-- requirements.txt                # Dependensi Python
|-- README.md                       # Dokumentasi proyek
|
|-- data/
|   |-- knowledge_base.json         # Gejala dan aturan diagnosis (RBR)
|   |-- case_library.json           # Database kasus (CBR, 32 kasus)
|
|-- src/
|   |-- __init__.py                 # Package init
|   |-- knowledge_base.py           # Kelas KnowledgeBase
|   |-- rbr_engine.py               # Kelas RBREngine (Forward Chaining)
|   |-- cbr_engine.py               # Kelas CBREngine (Weighted Nearest Neighbor)
|   |-- inference_engine.py         # Legacy inference engine (tidak digunakan)
|
|-- scripts/
|   |-- csv_to_json.py              # Utilitas konversi CSV ke JSON
|
|-- gejala.csv                      # Data gejala (format CSV asli)
|-- kerusakan.csv                   # Data kerusakan (format CSV asli)
```

---

## Prasyarat

- **Python** 3.10 atau lebih baru
- **pip** (Python package manager)
- Disarankan menggunakan virtual environment (venv, conda, dll.)

---

## Instalasi

1. Clone repository:

```bash
git clone <repository-url>
cd printer-diagnosis-expert-system
```

2. Buat dan aktifkan virtual environment (opsional tapi disarankan):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Instal dependensi:

```bash
pip install -r requirements.txt
```

---

## Menjalankan Aplikasi

Jalankan perintah berikut dari direktori root proyek:

```bash
python -m streamlit run app.py
```

Atau:

```bash
streamlit run app.py
```

Aplikasi akan terbuka secara otomatis di browser pada `http://localhost:8501`.

---

## Panduan Penggunaan

### Halaman Beranda (Dashboard)

Halaman utama menampilkan:
- Metrik ringkasan (jumlah gejala, aturan, kasus, dan metode)
- Dua kartu metode (RBR dan CBR) yang sejajar
- Tombol navigasi ke masing-masing metode diagnosis
- Referensi utama sistem

### Diagnosis RBR

1. Klik "Mulai Diagnosis RBR" atau pilih "RBR -- Rule-Based" di sidebar
2. Jawab setiap pertanyaan gejala dengan "Ya" atau "Tidak"
3. Setelah semua pertanyaan dijawab, hasil diagnosis akan ditampilkan
4. Hasil meliputi:
   - Diagnosis exact match (semua kondisi terpenuhi)
   - Diagnosis partial match (sebagian kondisi terpenuhi)
   - Inference trace (jejak penalaran langkah demi langkah)

### Diagnosis CBR

1. Klik "Mulai Diagnosis CBR" atau pilih "CBR -- Case-Based" di sidebar
2. Centang gejala yang dialami dari daftar checkbox (layout 3 kolom)
3. Klik "Cari Kasus Serupa"
4. Hasil meliputi:
   - Solusi yang diusulkan dari kasus paling mirip
   - Daftar kasus serupa dengan skor similarity
   - Detail perhitungan similarity (Weighted Nearest Neighbor)
   - Referensi URL yang terverifikasi
5. Opsional: Isi formulir untuk menyimpan kasus baru (Revise & Retain)

### Basis Pengetahuan

Menampilkan:
- Tabel semua gejala dengan kode, deskripsi, kategori, dan bobot
- Daftar aturan diagnosis (IF-THEN rules) dengan detail kondisi dan solusi

### Case Library

Menampilkan:
- Statistik case library (total kasus, berhasil, pending)
- Filter berdasarkan merek dan severity
- Detail setiap kasus dengan referensi URL yang dapat diklik

---

## Metode Rule-Based Reasoning (RBR)

### Definisi

Rule-Based Reasoning menggunakan aturan IF-THEN (production rules) untuk merepresentasikan pengetahuan pakar. Sistem mencocokkan fakta (gejala) yang diberikan pengguna dengan aturan-aturan yang ada untuk menghasilkan kesimpulan (diagnosis).

### Forward Chaining

Forward chaining (data-driven reasoning) bekerja sebagai berikut:

1. Kumpulkan fakta -- User menjawab pertanyaan tentang gejala
2. Cocokkan aturan -- Sistem memeriksa setiap rule apakah semua kondisi (antecedent) terpenuhi
3. Fire rule -- Jika semua kondisi terpenuhi, rule "terpicu" dan diagnosis dihasilkan
4. Ulangi -- Proses berlanjut untuk semua rule yang ada

### Representasi Aturan (AND Logic)

```
IF B1 (Printer tidak menyala)
   AND B2 (Lampu indikator berkedip)
THEN A1 (Kerusakan pada power supply)
```

Semua kondisi harus terpenuhi (AND logic) agar rule terpicu.

### Partial Matching

Ketika tidak ada rule yang 100% cocok, sistem menghitung persentase kecocokan untuk setiap rule dan menampilkan kemungkinan diagnosis berdasarkan kondisi yang sebagian terpenuhi.

### Inference Trace

Sistem menyediakan jejak inferensi yang menunjukkan langkah demi langkah proses penalaran, termasuk:
- Rule mana yang diperiksa
- Kondisi mana yang terpenuhi / tidak terpenuhi
- Apakah rule tersebut terpicu atau tidak

---

## Metode Case-Based Reasoning (CBR)

### Definisi

Case-Based Reasoning menyelesaikan masalah baru dengan mengingat dan mengadaptasi solusi dari masalah serupa yang pernah diselesaikan sebelumnya (Aamodt & Plaza, 1994).

### Siklus CBR (4R)

1. **RETRIEVE** -- Mengambil kasus-kasus paling mirip dari case library berdasarkan similarity
2. **REUSE** -- Mengadaptasi solusi dari kasus terdekat untuk masalah saat ini
3. **REVISE** -- Mengevaluasi dan menyesuaikan solusi yang diusulkan
4. **RETAIN** -- Menyimpan kasus baru yang berhasil ke case library untuk referensi di masa depan

### Metode Similarity: Weighted Nearest Neighbor

Perhitungan similarity menggunakan formula Weighted Nearest Neighbor:

```
Similarity(C_new, C_old) = Sum(wi * sim(fi_new, fi_old)) / Sum(wi)
```

Keterangan:
- `wi` = bobot fitur ke-i (diambil dari symptom weight di knowledge base)
- `sim(fi_new, fi_old)` = 1 jika gejala cocok di kedua kasus, 0 jika tidak
- `Sum(wi)` = total bobot semua fitur yang relevan (union dari gejala kedua kasus)

### Threshold Similarity

Sistem menggunakan threshold `0.4` (40%) sebagai batas minimum similarity. Kasus dengan similarity di bawah threshold tidak akan ditampilkan sebagai hasil.

### Tingkat Keyakinan

| Rentang Similarity | Tingkat Keyakinan | Keterangan |
|---|---|---|
| >= 90% | Sangat Tinggi | Solusi dapat diterapkan langsung |
| 70% - 89% | Tinggi | Solusi perlu sedikit penyesuaian |
| 50% - 69% | Sedang | Perlu evaluasi lebih lanjut |
| 40% - 49% | Rendah | Hanya sebagai referensi awal |

---

## Knowledge Base

### Format Data (knowledge_base.json)

Knowledge base disimpan dalam format JSON dengan dua bagian utama:

#### Gejala (Symptoms)

| Kode | Gejala | Kategori | Bobot |
|---|---|---|---|
| B1 | Printer tidak menyala | Power | 0.8 |
| B2 | Lampu indikator printer berkedip terus | Power | 0.6 |
| B3 | Printer tidak terdeteksi di komputer | Konektivitas | 0.7 |
| B4 | Printer tidak bisa menarik kertas | Mekanik | 0.7 |
| B5 | Hasil cetak buram atau tidak jelas | Kualitas Cetak | 0.5 |
| B6 | Tinta tidak keluar sama sekali | Kualitas Cetak | 0.9 |
| B7 | Kertas sering macet (paper jam) | Mekanik | 0.6 |
| B8 | Printer mencetak garis-garis | Kualitas Cetak | 0.5 |
| B9 | Muncul pesan error pada layar / software printer | Software | 0.4 |

Bobot (weight) digunakan oleh CBR engine untuk perhitungan Weighted Nearest Neighbor similarity. Semakin tinggi bobot, semakin signifikan gejala tersebut dalam menentukan kemiripan kasus.

#### Aturan Diagnosis (Rules)

| Kode | Kondisi | Diagnosis | Severity |
|---|---|---|---|
| A1 | B1 AND B2 | Kerusakan pada power supply | High |
| A2 | B3 AND B9 | Driver printer belum terinstal / rusak | Medium |
| A3 | B5 AND B6 AND B8 AND B9 | Cartridge / tinta bermasalah | Medium |
| A4 | B4 AND B7 | Roller atau mekanik penarik kertas rusak | High |
| A5 | B5 AND B6 AND B8 | Head printer kotor atau rusak | High |

---

## Case Library

### Deskripsi

Case library berisi 32 kasus diagnosis printer yang mencakup:

- **Merek**: HP, Epson, Canon, Brother, Samsung
- **Tipe**: InkJet, LaserJet
- **Severity**: Low, Medium, High
- **Outcome**: Success (semua kasus dalam library awal)

### Format Data (case_library.json)

Setiap kasus memiliki atribut berikut:

| Atribut | Deskripsi |
|---|---|
| `case_id` | Identifikasi unik kasus (C001, C002, ...) |
| `title` | Judul deskriptif kasus |
| `description` | Deskripsi detail kondisi printer |
| `printer_type` | Tipe printer (InkJet, LaserJet, dll.) |
| `brand` | Merek printer (HP, Epson, Canon, Brother, Samsung) |
| `symptoms` | Array kode gejala yang dialami (B1-B9) |
| `diagnosis` | Diagnosis yang diberikan |
| `solution` | Solusi yang diterapkan |
| `severity` | Tingkat keparahan (low, medium, high) |
| `outcome` | Hasil penanganan (success, failed, pending) |
| `date` | Tanggal kasus ditangani |
| `technician_notes` | Catatan teknisi |
| `references` | Array URL referensi yang terverifikasi |

### Referensi URL Terverifikasi

Setiap kasus dalam case library dilengkapi dengan referensi URL yang telah diverifikasi ketersediaannya. Sumber referensi yang digunakan:

- HP Printer Support: https://support.hp.com/us-en/printer
- HP Printing Errors: https://support.hp.com/us-en/topic/printing-errors
- Epson Printer Support: https://epson.com/Support/Printers/sh/s1
- Brother USA Support: https://www.brother-usa.com/support
- Samsung Support: https://www.samsung.com/us/support/
- Digital Trends (Common Printer Problems): https://www.digitaltrends.com/computing/common-printer-problems-and-how-to-fix-them/
- PrinterTesting.com: https://www.printertesting.com/
- Microsoft Learn (Print Spooler Reference): https://learn.microsoft.com/en-us/windows/win32/printdocs/printing-and-print-spooler-reference

---

## Referensi

### Buku dan Jurnal

1. Turban, E., Aronson, J.E., & Liang, T.P. (2005). *Decision Support Systems and Intelligent Systems* (7th ed.). Pearson Prentice Hall.
   - Referensi utama untuk konsep sistem pakar dan forward chaining.

2. Giarratano, J.C., & Riley, G.D. (2005). *Expert Systems: Principles and Programming* (4th ed.). Thomson Course Technology.
   - Referensi untuk implementasi rule-based expert systems.

3. Aamodt, A., & Plaza, E. (1994). Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches. *AI Communications*, 7(1), 39-59.
   - Paper fundamental untuk CBR dan siklus 4R (Retrieve-Reuse-Revise-Retain).

4. Kolodner, J. (1993). *Case-Based Reasoning*. Morgan Kaufmann Publishers.
   - Referensi komprehensif untuk teori dan aplikasi CBR.

5. Watson, I. (1997). *Applying Case-Based Reasoning: Techniques for Enterprise Systems*. Morgan Kaufmann Publishers.
   - Referensi untuk penerapan CBR di sistem enterprise.

### Teknologi

- Python (https://www.python.org/)
- Streamlit (https://streamlit.io/)

---

## Lisensi

Proyek ini dibuat untuk keperluan akademis dan pembelajaran.
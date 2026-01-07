# 🌏 Air Quality Analysis Dashboard – Beijing

Proyek ini merupakan **project terbaru** saya berupa *end-to-end data analysis* yang berfokus pada **kualitas udara di Beijing**. Project ini mencakup proses **Data Wrangling**, **Exploratory Data Analysis (EDA)**, hingga pembuatan **dashboard interaktif menggunakan Streamlit** untuk memantau kondisi polusi udara secara visual dan informatif.

Project ini dikembangkan sebagai **tugas akhir kelas "Belajar Analisis Data dengan Python" – Dicoding**, sekaligus sebagai **portfolio Data Analyst**.

---

## 🚀 Live Demo (Preview Dashboard)

> Berikut adalah tampilan demo dashboard Air Quality Beijing:

![Air Quality Dashboard Demo](dashboardaq.gif)

Dashboard menyajikan insight utama seperti:

* Tren PM2.5 dan PM10 dari waktu ke waktu
* Perbandingan kualitas udara antar stasiun
* Distribusi tingkat polusi
* Analisis kondisi udara berdasarkan waktu

---

## 🧠 Objectives

* Melakukan pembersihan dan transformasi data kualitas udara
* Mengeksplorasi pola polusi udara di Beijing
* Menyajikan insight dalam bentuk dashboard interaktif
* Mengembangkan dashboard yang *user-friendly* dan informatif

---

## 🗂️ Project Structure

```
air-quality-dashboard/
│
├── data/                # Dataset hasil preprocessing
├── notebook.ipynb       # Data Wrangling & EDA
├── dashboard.py         # Streamlit dashboard
├── dashboardaq.gif      # Demo dashboard
├── requirements.txt     # Library dependencies
├── README.md            # Project documentation
```

---

## 👤 Identitas Pemilik

* **Nama**: Muhammad Ridwan Alrafi
* **Email**: [Muhammad.alrafi@mhs.unsoed.ac.id](mailto:Muhammad.alrafi@mhs.unsoed.ac.id)
* **Dicoding Username**: muhammad_rid

---

## ⚙️ Setup Environment

### Menggunakan Anaconda

```
conda create --name air-quality-ds python=3.10
conda activate air-quality-ds
pip install -r requirements.txt
```

### Menggunakan Shell / Terminal

```
mkdir proyek_air_quality
cd proyek_air_quality
pipenv install
pipenv shell
pip install -r requirements.txt
```

---

## ▶️ Run Streamlit App

```
streamlit run dashboard.py
```

Aplikasi akan berjalan secara lokal dan dapat diakses melalui browser.

---

## 🛠️ Tech Stack

* Python
* Pandas & NumPy
* Matplotlib & Seaborn
* Streamlit
* Jupyter Notebook

---

## 📌 Notes

Project ini ditujukan untuk kebutuhan **pembelajaran, evaluasi, dan portfolio**. Dataset yang digunakan berasal dari sumber pembelajaran Dicoding.

---

✨ *Feel free to explore the project and give feedback!*

import streamlit as st
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# KONFIGURASI HALAMAN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Skrining Gizi Anak Umum (Usia 1 - 12 Tahun)",
    page_icon="👦",
    layout="wide"
)

st.title("👦 Sistem Cerdas Skrining Risiko Kekurangan / Kelebihan Gizi Anak (Usia 1 - 12 Tahun)")
st.write("Expert System untuk evaluasi status gizi, pola konsumsi, aktivitas fisik, dan kesehatan anak secara umum.")
st.caption("⚠️ **Disclaimer:** Aplikasi ini adalah media skrining awal dan edukasi mandiri, bukan pengganti diagnosis medis resmi dari dokter spesialis.")

st.markdown("---")

# ---------------------------------------------------------
# KUESIONER MULTI-DIMENSI ANAK UMUR 1 - 12 TAHUN
# ---------------------------------------------------------
col_1, col_2 = st.columns(2)

with col_1:
    st.subheader("📋 Bagian 1: Data Identitas & Antropometri")
    nama = st.text_input("Nama Anak", "Alya Zahra")
    
    # Pilihan kelompok usia agar lebih fleksibel (Balita vs Anak Sekolah)
    kategori_usia = st.selectbox("Kelompok Usia Anak:", [
        "Balita (1 - 5 tahun / 12 - 60 bulan)", 
        "Anak Usia Sekolah / Pra-Remaja (6 - 12 tahun)"
    ])
    
    if kategori_usia == "Balita (1 - 5 tahun / 12 - 60 bulan)":
        usia_tahun_hitung = st.number_input("Usia (dalam Bulan)", min_value=12, max_value=60, value=36)
        label_usia_str = f"{usia_tahun_hitung} Bulan"
    else:
        usia_tahun_hitung = st.number_input("Usia (dalam Tahun)", min_value=6, max_value=12, value=8)
        label_usia_str = f"{usia_tahun_hitung} Tahun"

    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    berat = st.number_input("Berat Badan Aktual (kg)", min_value=5.0, max_value=60.0, value=22.0, step=0.1)
    tinggi = st.number_input("Tinggi Badan Aktual (cm)", min_value=70.0, max_value=160.0, value=120.0, step=0.5)

    st.markdown("---")
    st.subheader("🥗 Bagian 2: Pola Konsumsi & Kualitas Makanan")
    frekuensi_protein_hewani = st.selectbox("Konsumsi Protein Hewan (Ikan/Telur/Daging/Ayam/Susu):", [
        "Setiap hari (Minimal 2 sumber berbeda)", 
        "Setiap hari (Hanya 1 sumber)", 
        "2-3 kali dalam seminggu", 
        "Jarang / Sangat terbatas"
    ])
    konsumsi_junkfood = st.selectbox("Konsumsi Makanan Instan / Manis / Junk Food / Minuman Kemasan:", [
        "Jarang / Tidak pernah", 
        "Kadang-kadang (1-2 kali seminggu)", 
        "Sering (Hampir setiap hari ngemil makanan manis/junk food)"
    ])
    konsumsi_sayur_buah = st.selectbox("Konsumsi Sayur & Buah Segar:", [
        "Rutin setiap hari", 
        "Kadang-kadang (suka pilih-pilih sayur)", 
        "Sangat jarang / Menolak makan sayur dan buah"
    ])

with col_2:
    st.subheader("🍽️ Bagian 3: Perilaku Makan & Aktivitas")
    perilaku_makan = st.selectbox("Kebiasaan / Perilaku Makan Anak:", [
        "Makan teratur, porsi cukup, tidak rewel", 
        "Pilih-pilih makanan (picky eater) atau porsi terlalu sedikit", 
        "Sangat sulit makan / Sering menolak makanan utama"
    ])
    aktivitas_fisik = st.selectbox("Aktivitas Fisik / Olahraga / Bermain Aktif:", [
        "Aktif bergerak / Sering bermain di luar ruangan setiap hari", 
        "Cukup aktif (bermain di rumah/sekolah)", 
        "Kurang aktif / Lebih banyak duduk diam di dalam ruangan"
    ])
    screen_time = st.selectbox("Durasi Penggunaan Gadget / TV per Hari:", [
        "Kurang dari 1 jam per hari", 
        "1 - 3 jam per hari", 
        "Lebih dari 3 jam per hari (lama di depan layar)"
    ])

    st.markdown("---")
    st.subheader("🦠 Bagian 4: Riwayat Kesehatan & Keluhan")
    riwayat_sakit = st.selectbox("Kondisi Kesehatan Umum (3 bulan terakhir):", [
        "Sehat bugar / Jarang sakit", 
        "Pernah sakit ringan (batuk/pilek/diare) lalu cepat sembuh", 
        "Sering sakit berulang / Mengalami gangguan pencernaan kronis"
    ])
    keluhan_fisik = st.multiselect("Apakah anak mengalami keluhan berikut? (Pilih jika ada):", [
        "Sering tampak lesu / cepat lelah saat beraktivitas",
        "Konsentrasi belajar menurun / sering mengantuk di siang hari",
        "Sering mengeluh nyeri perut / masalah BAB (konstipasi/diare)",
        "Pertumbuhan tinggi badan terlihat jauh tertinggal dari teman sebayanya"
    ])

st.markdown("---")

# ---------------------------------------------------------
# ENGINE SISTEM CERDAS (RULE-BASED INFERENCE UNTUK ANAK UMUM)
# ---------------------------------------------------------
def jalankan_sistem_pakar_umum(
    kategori, usia_val, bb, tb, jkel, pakan_hewan, junkfood, sayur_buah,
    perilaku, aktivitas, gadget, sakit, keluhan
):
    skor_risiko = 0
    log_analisis = []

    # 1. Estimasi Standar Antropometri Sederhana Berdasarkan Kelompok Usia
    if "Balita" in kategori:
        # usia_val dalam bulan (12 - 60)
        bb_ideal = (usia_val * 0.22) + 8
        tb_ideal = (usia_val * 0.4) + 75
    else:
        # usia_val dalam tahun (6 - 12)
        # Rumus estimasi kasar berat/tinggi anak sekolah
        bb_ideal = (usia_val * 2.5) + 8
        tb_ideal = (usia_val * 6) + 75

    rasio_bb = bb / bb_ideal
    rasio_tb = tb / tb_ideal

    # Deteksi Masalah Berat Badan (Bisa Underweight atau Overweight/Obesity)
    if rasio_bb < 0.80:
        skor_risiko += 4
        log_analisis.append("⚠️ **Berat Badan:** Terlalu rendah dibandingkan estimasi ideal (Indikasi Gizi Kurang / Underweight).")
    elif rasio_bb > 1.30:
        skor_risiko += 3
        log_analisis.append("⚠️ **Berat Badan:** Di atas rata-rata normal (Waspada Risiko Kelebihan Berat Badan / Obesitas).")
    elif rasio_bb < 0.90:
        skor_risiko += 2
        log_analisis.append("⚠️ **Berat Badan:** Sedikit di bawah standar ideal.")

    # Deteksi Tinggi Badan (Potensi Stunting / Pendek)
    if rasio_tb < 0.90:
        skor_risiko += 4
        log_analisis.append("⚠️ **Tinggi Badan:** Signifikan di bawah standar (Indikasi Potensi Pertumbuhan Terhambat / Stunting).")

    # 2. Analisis Pola Makan
    if "2-3 kali" in pakan_hewan:
        skor_risiko += 1
        log_analisis.append("📌 **Protein Hewani:** Frekuensi konsumsi protein harian kurang optimal.")
    elif "Jarang" in pakan_hewan:
        skor_risiko += 3
        log_analisis.append("🥩 **Protein Hewani:** Defisit protein hewani yang merupakan zat gizi esensial utama.")

    if "Sering" in junkfood:
        skor_risiko += 3
        log_analisis.append("🍔 **Junk Food:** Konsumsi makanan instan/manis tinggi kalori kosong (risiko malnutrisi atau obesitas).")

    if "Sangat jarang" in sayur_buah:
        skor_risiko += 2
        log_analisis.append("🥦 **Serat & Vitamin:** Kurang asupan serat, vitamin, dan mineral dari sayur/buah.")

    # 3. Analisis Perilaku & Gaya Hidup
    if "Sangat sulit" in perilaku:
        skor_risiko += 2
        log_analisis.append("🍽️ **Perilaku Makan:** Mengalami kesulitan makan yang berdampak pada asupan nutrisi harian.")
    if "Kurang aktif" in aktivitas:
        skor_risiko += 1
        log_analisis.append("🛋️ **Aktivitas Fisik:** Kurangnya aktivitas fisik dapat memengaruhi kebugaran dan metabolisme.")
    if "Lebih dari 3 jam" in gadget:
        skor_risiko += 2
        log_analisis.append("📱 **Screen Time:** Durasi penggunaan gadget berlebih memicu gaya hidup sedentari (kurang gerak) dan gangguan pola makan.")

    # 4. Riwayat Kesehatan & Keluhan
    if "Sering sakit" in sakit:
        skor_risiko += 3
        log_analisis.append("🦠 **Kesehatan Umum:** Infeksi atau gangguan pencernaan berulang memengaruhi penyerapan nutrisi.")
    
    if len(keluhan) > 0:
        skor_risiko += (len(keluhan) * 1)
        for k in keluhan:
            log_analisis.append(f"⚠️ **Keluhan Klinis:** {k}")

    # Penentuan Kategori Keputusan Akhir
    if skor_risiko >= 8:
        kategori_hasil = "Risiko Tinggi (Gangguan Gizi / Pertumbuhan Bermasalah)"
        warna = "red"
        rekomendasi = [
            "**Segera konsultasikan kondisi anak ke Dokter Spesialis Anak atau Ahli Gizi (Nutrisionis)** untuk pemeriksaan kurva pertumbuhan antropometri resmi.",
            "Lakukan evaluasi menyeluruh terhadap menu harian, porsi, dan kebiasaan jajan anak.",
            "Periksa kemungkinan adanya gangguan penyerapan atau penyakit penyerta jika anak sering mengeluh sakit perut atau lemas.",
            "Batasi total waktu layar (*screen time*) dan perbanyak aktivitas fisik luar ruangan."
        ]
    elif skor_risiko >= 4:
        kategori_hasil = "Risiko Sedang (Waspada Pola Gizi & Gaya Hidup)"
        warna = "orange"
        rekomendasi = [
            "Tingkatkan variasi menu makanan rumah yang kaya protein hewani (ikan, telur, daging) dan kurangi makanan instan/manis.",
            "Atur jadwal makan anak secara konsisten setiap hari tanpa distraksi gadget.",
            "Pantau berat dan tinggi badan anak secara berkala setiap 1-3 bulan di fasilitas kesehatan terdekat.",
            "Ajak anak melakukan aktivitas fisik atau olahraga ringan secara rutin."
        ]
    else:
        kategori_hasil = "Risiko Rendah (Status Gizi & Tumbuh Kembang Cenderung Normal)"
        warna = "green"
        rekomendasi = [
            "Pertahankan pola makan gizi seimbang serta kebiasaan hidup aktif harian.",
            "Tetap lakukan pemantauan tumbuh kembang anak secara berkala.",
            "Pastikan anak mendapatkan waktu istirahat (tidur) yang cukup setiap harinya."
        ]

    return kategori_hasil, warna, skor_risiko, log_analisis, rekomendasi, bb_ideal, tb_ideal

# ---------------------------------------------------------
# TOMBOL EKSEKUSI & TAMPILAN OUTPUT
# ---------------------------------------------------------
if st.button("🚀 Jalankan Analisis Sistem Cerdas", type="primary", use_container_width=True):
    kategori_hasil, warna, total_skor, logs, rekomendasi_list, bb_ideal, tb_ideal = jalankan_sistem_pakar_umum(
        kategori_usia, usia_tahun_hitung, berat, tinggi, jenis_kelamin,
        frekuensi_protein_hewani, konsumsi_junkfood, konsumsi_sayur_buah,
        perilaku_makan, aktivitas_fisik, screen_time, riwayat_sakit, keluhan_fisik
    )

    st.markdown("---")
    st.subheader(f"📊 Hasil Evaluasi Sistem Pakar untuk: {nama}")

    if warna == "red":
        st.error(f"**Kategori:** {kategori_hasil} (Total Skor Risiko: {total_skor})")
    elif warna == "orange":
        st.warning(f"**Kategori:** {kategori_hasil} (Total Skor Risiko: {total_skor})")
    else:
        st.success(f"**Kategori:** {kategori_hasil} (Total Skor Risiko: {total_skor})")

    col_res1, col_res2 = st.columns(2)

    with col_res1:
        st.markdown("### 🔎 Temuan Rule-Based Inference:")
        if logs:
            for l in logs:
                st.write(f"- {l}")
        else:
            st.write("- Tidak ditemukan indikator risiko signifikan dari parameter yang dimasukkan.")

        st.markdown("### 💡 Saran Tindak Lanjut:")
        for r in rekomendasi_list:
            st.write(f"- {r}")

    with col_res2:
        st.markdown("### 📈 Grafik Komparasi Fisik Aktual vs Estimasi Ideal")
        fig, ax = plt.subplots(figsize=(5, 3))
        
        labels = ['Berat Badan (kg)', 'Tinggi Badan (cm) / 5']
        aktual = [berat, tinggi / 5]
        ideal = [bb_ideal, tb_ideal / 5]
        
        x = range(len(labels))
        width = 0.35
        
        ax.bar([p - width/2 for p in x], aktual, width, label='Aktual Anak', color='#ff7f0e')
        ax.bar([p + width/2 for p in x], ideal, width, label='Estimasi Ideal', color='#1f77b4')
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        st.pyplot(fig)
        st.caption("*Catatan: Skala tinggi badan disesuaikan agar proporsional dalam satu grafik batang.")

    st.markdown("---")
    with st.expander("📚 Penjelasan Sistem Cerdas untuk Anak Usia Umum"):
        st.markdown("""
        * **Fleksibilitas Kategori Usia:** Sistem secara otomatis mendeteksi kelompok usia (apakah anak balita atau anak usia sekolah dasar) guna menyesuaikan standar estimasi antropometri.
        * **Multidimensi Penilaian:** Tidak hanya melihat berat dan tinggi badan, sistem juga menganalisis gaya hidup modern seperti konsumsi *junk food*, durasi *screen time* (gadget), tingkat aktivitas fisik, hingga keluhan klinis harian.
        * **Penerapan Rule-Based System:** Akumulasi poin risiko dievaluasi menggunakan aturan logika (*IF-THEN rules*) untuk menghasilkan kategori risiko dan saran tindak lanjut yang akurat.
        """)
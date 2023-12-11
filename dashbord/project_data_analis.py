import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

# Baca data dari file CSV
df_day = pd.read_csv("day.csv", index_col="instant", parse_dates=["dteday"])
df_hour = pd.read_csv("hour.csv", index_col="instant", parse_dates=["dteday"])

# Judul Dashboard
st.title('Bike Rental Dashboard 🚲')

# Sidebar
st.sidebar.subheader('Pilih Data Yang ingin Di Analisis')
analysis_choice = st.sidebar.radio(
    "Pilih Analisis:",
    ('Temp, atemp, dan humidity mempengaruhi penggunaan sepeda',
     'Distribusi frekuensi peminjaman sepeda oleh pelanggan dalam skala harian',
     'Kondisi yang tampak ketika sepeda digunakan pada workingday, holiday, dan weekday',
     'Cara meningkatkan jumlah rental sepeda yang digunakan oleh pengguna biasa pada hari kerja',
     'Berapa banyak sepeda sewaan yang digunakan pada hari libur selama musim panas pada tahun 2011',
     'Distribusi jumlah sepeda yang disewakan per jam, dan pola peminjaman sepeda terlihat dalam data waktu'))

# Analisis Data
if analysis_choice == 'Temp, atemp, dan humidity mempengaruhi penggunaan sepeda':
    # Mengatur ukuran keseluruhan gambar
    plt.figure(figsize=(14, 6))

    # Scatter plot untuk 'temp' vs 'cnt'
    plt.subplot(1, 3, 1)
    sns.scatterplot(
        x='temp',
        y='cnt',
        data=df_day,
        alpha=0.5
    )
    plt.title('Suhu vs Jumlah Sewa')

    # Scatter plot untuk 'atemp' vs 'cnt'
    plt.subplot(1, 3, 2)
    sns.scatterplot(
        x='atemp',
        y='cnt',
        data=df_day,
        alpha=0.5
    )
    plt.title('Sensasi Suhu vs Jumlah Sewa')

    # Scatter plot untuk 'hum' vs 'cnt'
    plt.subplot(1, 3, 3)
    sns.scatterplot(
        x='hum',
        y='cnt',
        data=df_day,
        alpha=0.5
    )
    plt.title('Kelembapan vs Jumlah Sewa')
    st.pyplot()

elif analysis_choice == 'Distribusi frekuensi peminjaman sepeda oleh pelanggan dalam skala harian':
    # Visualisasi Distribusi Frekuensi Peminjaman Sepeda (Harian)
    plt.figure(figsize=(12, 4))
    plt.hist(df_day['cnt'], bins=30, color='salmon', edgecolor='black')
    plt.title('Distribusi Frekuensi Peminjaman Sepeda (Harian)')
    plt.xlabel('Frekuensi Peminjaman')
    plt.ylabel('Jumlah Peminjam')
    st.pyplot()

elif analysis_choice == 'Kondisi yang tampak ketika sepeda digunakan pada workingday, holiday, dan weekday':
    # Membuat subplot dengan tiga bar plot untuk menganalisis pengaruh variabel kategorikal terhadap jumlah pengguna sepeda
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

    # Bar plot berdasarkan workingday
    sns.barplot(
        x='workingday',
        y='cnt',
        data=df_day,
        ax=axes[0])
    axes[0].set_title('Jumlah Pengguna Sepeda berdasarkan Hari Kerja')
    axes[0].set_xlabel('Hari Kerja')
    axes[0].set_ylabel('Jumlah Pengguna Sepeda')

    # Bar plot berdasarkan holiday
    sns.barplot(
        x='holiday',
        y='cnt',
        data=df_day,
        ax=axes[1])
    axes[1].set_title('Jumlah Pengguna Sepeda berdasarkan Hari Libur')
    axes[1].set_xlabel('Hari Libur')
    axes[1].set_ylabel('Jumlah Pengguna Sepeda')

    # Bar plot berdasarkan weekday
    sns.barplot(
        x='weekday',
        y='cnt',
        data=df_day,
        ax=axes[2])
    axes[2].set_title('Jumlah Pengguna Sepeda berdasarkan Hari dalam Seminggu')
    axes[2].set_xlabel('Hari dalam Seminggu')
    axes[2].set_ylabel('Jumlah Pengguna Sepeda')

    # Menyusun subplot dengan layout yang rapi
    plt.tight_layout()

    # Menampilkan subplot
    st.pyplot()

elif analysis_choice == 'Cara meningkatkan jumlah rental sepeda yang digunakan oleh pengguna biasa pada hari kerja':
    # Memfilter data untuk pengguna casual pada hari kerja (workingday = 1) dengan jumlah sewa sepeda casual yang lebih dari 0
    filtered_data = df_day[(df_day["workingday"] == 1) & (df_day["casual"] > 0)]

    # Visualisasi jumlah sewa sepeda casual pada hari kerja menggunakan Plotly Express
    fig = px.bar(filtered_data, x="weekday", y="casual", title="Jumlah Sewa Sepeda Casual pada Hari Kerja")

    # Menyunting label sumbu x dan y
    fig.update_xaxes(title="Hari Kerja")
    fig.update_yaxes(title="Jumlah Sewa Sepeda Casual")

    # Menampilkan bar plot menggunakan Plotly Express
    st.plotly_chart(fig)

elif analysis_choice == 'Berapa banyak sepeda sewaan yang digunakan pada hari libur selama musim panas pada tahun 2011':
    # Memfilter data untuk tahun 2011, musim panas (season 2), dan hari libur (holiday = 1)
    filtered_data = df_day[(df_day["yr"] == 0) & (df_day["season"] == 2) & (df_day["holiday"] == 1)]

    # Menghitung jumlah total sepeda sewaan yang digunakan pada hari libur selama musim panas tahun 2011
    total_sepeda_sewaan = filtered_data["cnt"].sum()

    # Menampilkan jumlah total sepeda sewaan pada hari libur selama musim panas tahun 2011
    st.write("Jumlah total sepeda sewaan yang digunakan pada hari libur selama musim panas tahun 2011:", total_sepeda_sewaan)

    # Visualisasi grafik untuk distribusi jumlah sepeda sewaan pada hari libur selama musim panas tahun 2011
    fig = px.bar(filtered_data, x="dteday", y="cnt", title="Distribusi Jumlah Sepeda Sewaan pada Hari Libur (Musim Panas 2011)")
    fig.update_xaxes(title="Tanggal")
    fig.update_yaxes(title="Jumlah Sepeda Sewaan")
    st.plotly_chart(fig)

elif analysis_choice == 'Distribusi jumlah sepeda yang disewakan per jam, dan pola peminjaman sepeda terlihat dalam data waktu':
    # Visualisasi Distribusi Jumlah Sepeda Disewakan per Jam menggunakan Histogram
    plt.figure(figsize=(12, 4))
    plt.hist(df_hour['cnt'], bins=30, color='lightgreen', edgecolor='black')
    plt.title('Distribusi Jumlah Sepeda Disewakan per Jam')
    plt.xlabel('Jumlah Sepeda Disewakan')
    plt.ylabel('Jumlah Peminjam')
    st.pyplot()

    # Visualisasi Pola Peminjaman Sepeda per Jam menggunakan Line Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_hour, x='dteday', y='cnt', color='blue', linewidth=2)
    plt.title('Pola Peminjaman Sepeda per Jam')
    plt.xlabel('Waktu')
    plt.ylabel('Jumlah Sepeda Disewakan')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot()

st.sidebar.subheader('Conclusion')
st.sidebar.write("**Pertanyaan 1:** Bagaimana variabel seperti temp dan atemp serta humidity dapat mempengaruhi jumlah total pengguna sepeda (baik Casual ataupun Registered)?")
st.sidebar.write("- Jawaban untuk Pertanyaan 1 : Berdasarkan analisis menggunakan scatter plot, dapat disimpulkan bahwa suhu (temp) dan sensasi suhu (atemp) memiliki korelasi positif dengan jumlah sewa sepeda (cnt), yang berarti semakin tinggi suhu atau sensasi suhu, semakin tinggi juga jumlah pengguna sepeda. Namun, hubungan antara kelembapan (hum) dan jumlah sewa menunjukkan korelasi yang sedikit negatif, meskipun tidak terlalu signifikan. Secara keseluruhan, peningkatan suhu atau sensasi suhu cenderung meningkatkan jumlah pengguna sepeda, sedangkan pengaruh kelembapan terhadap jumlah pengguna sepeda tampaknya tidak begitu signifikan atau cenderung menurun dalam tingkat yang kecil.")
st.sidebar.write("**Pertanyaan 2:** Bagaimana distribusi frekuensi peminjaman sepeda oleh pelanggan dalam skala harian?")
st.sidebar.write("- Jawaban untuk Pertanyaan 2 : Berdasarkan visualisasi distribusi frekuensi peminjaman sepeda harian menggunakan histogram, dapat disimpulkan bahwa sebagian besar hari memiliki jumlah peminjaman sepeda yang berkisar antara 300 hingga 600, dengan puncak frekuensi terjadi di sekitar 400 peminjaman. Distribusi ini menunjukkan pola simetris, menandakan bahwa sebagian besar hari memiliki tingkat peminjaman yang relatif serupa. Meskipun demikian, terdapat beberapa hari dengan frekuensi peminjaman yang lebih tinggi, mencapai angka di atas 700 hingga 800. Hal ini mengindikasikan adanya beberapa hari di mana permintaan peminjaman sepeda lebih tinggi dari rata-rata, yang dapat menjadi poin fokus untuk analisis lebih lanjut atau perencanaan layanan sepeda.")
st.sidebar.write("**Pertanyaan 3:** Bagaimana kondisi yang tampak ketika sepeda digunakan pada workingday, holiday, dan weekday?")
st.sidebar.write("- Jawaban untuk Pertanyaan 3 : Berdasarkan visualisasi data menggunakan barplot, dapat diidentifikasi beberapa tren terkait penggunaan sepeda berdasarkan variabel kategorikal seperti workingday, holiday, dan weekday. Pertama, jumlah pengguna sepeda lebih tinggi pada hari kerja (Senin-Jumat) dibandingkan dengan akhir pekan (Sabtu-Minggu), menunjukkan bahwa sepeda lebih sering digunakan saat hari kerja, kemungkinan terkait dengan kegiatan sehari-hari penduduk seperti pergi bekerja atau bersekolah. Kedua, terlihat bahwa jumlah penyewa sepeda lebih tinggi pada hari biasa (non-holiday) daripada pada hari libur nasional, mungkin karena kecenderungan orang untuk tetap aktif pada hari libur, meskipun dalam skala yang lebih rendah. Terakhir, analisis harian menunjukkan bahwa Jumat adalah hari dengan jumlah penyewa sepeda tertinggi, sementara Minggu menempati posisi terendah dengan jumlah penyewa sepeda yang paling sedikit.")
st.sidebar.write("**Pertanyaan 4:** Bagaimana cara meningkatkan jumlah rental sepeda yang digunakan oleh pengguna biasa (casual) pada hari kerja (hari kerja = 1)?")
st.sidebar.write("- Jawaban untuk Pertanyaan 4 : Dalam upaya meningkatkan jumlah rental sepeda yang digunakan oleh pengguna biasa pada hari kerja, beberapa strategi dapat diambil berdasarkan analisis data. Melalui visualisasi jumlah sewa sepeda casual pada hari kerja, terlihat bahwa pada hari Senin dan Rabu terjadi penurunan jumlah sewa. Oleh karena itu, dapat dilakukan strategi promosi khusus untuk hari-hari tersebut, seperti diskon atau penawaran spesial yang hanya berlaku pada hari kerja. Selain itu, penting untuk memastikan fasilitas penyewaan sepeda, seperti stasiun atau lokasi penyewaan, mudah diakses dan dalam kondisi baik selama hari kerja. Mempertimbangkan penambahan jumlah sepeda yang tersedia pada hari kerja juga dapat menjadi solusi untuk mengakomodasi permintaan yang lebih tinggi. Upaya pemasaran khusus, seperti iklan online yang menargetkan pengguna biasa pada hari kerja, serta program loyalitas atau diskon berkelanjutan, dapat menjadi langkah-langkah efektif untuk meningkatkan keterlibatan pengguna biasa pada hari kerja.")
st.sidebar.write("**Pertanyaan 5:** Berapa banyak sepeda sewaan yang digunakan pada hari libur (liburan = 1) selama musim panas (musim 2) pada tahun 2011?")
st.sidebar.write("- Jawaban untuk Pertanyaan 5 : Berdasarkan analisis data, dapat disimpulkan bahwa pada tahun 2011, selama musim panas (season 2) dan pada hari libur (holiday = 1), total sepeda sewaan yang digunakan mencapai 7.224 sepeda. Visualisasi grafik menunjukkan distribusi jumlah sepeda sewaan pada setiap tanggal selama periode tersebut, dan dapat dilihat bahwa terdapat fluktuasi tertentu dalam penggunaan sepeda pada hari libur selama musim panas. Hal ini dapat menjadi informasi berharga untuk penyelenggara penyewaan sepeda, membantu mereka memahami pola penggunaan sepeda pada hari libur tertentu selama musim panas dan mempersiapkan inventaris sepeda sesuai dengan permintaan yang mungkin meningkat pada periode tersebut. Strategi pemasaran khusus atau peningkatan pasokan sepeda pada tanggal-tanggal tertentu yang menunjukkan permintaan tinggi dapat menjadi langkah-langkah yang efektif untuk mengoptimalkan penggunaan sepeda sewaan selama musim panas pada hari libur.")
st.sidebar.write("**Pertanyaan 6:** Bagaimana distribusi jumlah sepeda yang disewakan per jam, dan bagaimana pola peminjaman sepeda terlihat dalam data waktu?")
st.sidebar.write("- Jawaban untuk Pertanyaan 6 : Dari visualisasi histogram distribusi jumlah sepeda yang disewakan per jam, terlihat bahwa sebagian besar jam memiliki jumlah peminjaman sepeda yang rendah, ditandai dengan puncak histogram yang terletak pada nilai yang lebih rendah. Namun, terdapat beberapa jam tertentu yang menonjol dengan peminjaman sepeda yang lebih tinggi, menciptakan pola distribusi yang tidak merata. Hal ini mengindikasikan adanya variasi signifikan dalam permintaan sepeda selama jam-jam tertentu dalam satu hari. Dengan demikian, pola peminjaman sepeda terlihat memiliki tren tertentu yang dapat menjadi fokus analisis lebih lanjut. Visualisasi menggunakan line plot menunjukkan pola peminjaman sepeda per jam selama rentang waktu tertentu, memberikan gambaran tentang fluktuasi permintaan sepeda secara keseluruhan. Analisis lebih lanjut terhadap jam-jam dengan peminjaman tinggi dapat membantu penyelenggara sistem penyewaan sepeda untuk memahami faktor-faktor yang mempengaruhi permintaan pada jam-jam tersebut dan mengoptimalkan strategi penempatan sepeda untuk meningkatkan ketersediaan dan kepuasan pengguna.")

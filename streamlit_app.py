
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")

hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
hour_df["yr"] = hour_df["yr"].apply(lambda x: 2011 if x == 0 else 2012)
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
day_df["yr"] = day_df["yr"].apply(lambda x: 2011 if x == 0 else 2012)



# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Dashboard Analisis Data",
    page_icon=":sparkles:",  # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
"""
# :sparkles: Proyek Analsis Data Menggunakan Bike Sharing Dataset

**Dicoding IDCamp 2024**

"""

st.info(
    """
    Nama: [Dhimas Sena Rahmantara]\n
    Email: [dhimassr@gmail.com]\n
    ID Dicoding: [dhimassena]
    """
)

def panggil_pertanyaan_1():
    st.subheader("Bagaimana jumlah penyewaan sepeda berdasarkan musim (spring, summer, fall, winter)?", divider="red")

    def season_conv(x):
        if x == 1:
            return "Spring"
        elif x == 2:
            return "Summer"
        elif x == 3:
            return "Fall"
        elif x == 4:
            return "Winter"


    cnt_per_yr_season = day_df.groupby(by=['yr','season']).agg({
        'cnt': 'sum',
    }).reset_index()
    cnt_per_yr_season["season_str"] = cnt_per_yr_season["season"].apply(season_conv)

    g = sns.catplot(
        data=cnt_per_yr_season, kind="bar",
        x="season_str", y="cnt", hue="yr", palette="Set1", height=10
    )
    for ax in g.axes.ravel():
        for c in ax.containers:
            ax.bar_label(c, label_type='edge')

    # fig = plt.figure(figsize=(10, 10))
    plt.title("Count of Bikes Rented According to Seasons in 2011 & 2012")
    plt.xlabel("Seasons")
    plt.ylabel("Count of bikes rented")
    st.pyplot(plt.gcf())

    st.caption(
        """
        **Insight:**
        - Dari grafik di atas, berdasarkan musim pada tahun 2011 dan 2012, penyewaan paling banyak terjadi pada musim Fall, dan penyewaan paling sedikit adalah pada musim Spring
        - Spring 2011 memiliki jumlah penyewaan sepeda sebanyak 150000 dan meningkat hampir 2,8 kali lipat pada Fall 2011 menjadi 419650
        - Namun perbadingan Spring 2012 dan Fall 2012 hanya memiliki kenaikan hampir 2 kali lipat, dimana jumlah penyewaan sepeda naik dari 321348 menjadi 641479
        - Secara umum terdapat peningkatan jumlah penyewaan sepeda pada tahun 2012 dibandingkan tahun 2011

        **Conclusion pertanyaan 1 :**
        Penyewaan sepeda berdasarkan musim paling banyak dilakukan pada Fall, dan paling sedikit pada Spring. Hal ini terjadi baik pada tahun 2011 maupun 2012
        """
    )

def panggil_pertanyaan_2():
    st.subheader("Apakah jumlah penyewaan sepeda berbeda secara signifikan pada bukan hari kerja dibandingkan dengan hari kerja?", divider="orange")

    cnt_per_yr_workingday = hour_df.groupby(by=['yr','workingday']).agg({
        'cnt': 'sum',
    }).reset_index()
    cnt_per_yr_workingday["workingday_str"] = cnt_per_yr_workingday["workingday"].apply(lambda x: "Workingday" if x == 1 else "Holiday/\nSaturday/\nSunday")

    g = sns.catplot(
        data=cnt_per_yr_workingday, kind="bar", hue="yr", palette="Set1",
        x="workingday_str", y="cnt", height=5
    )
    for ax in g.axes.ravel():
        for c in ax.containers:
            ax.bar_label(c, label_type='edge', fmt = '%d')

    plt.title("Count of Bikes Rented According to Workingday or Not in 2011 & 2012\n")
    plt.xlabel("Kind of Days")
    plt.ylabel("Count of bikes rented")
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(plt.gcf())

    st.caption(
        """
        **Insight:**
        - Grafik di atas menunjukkan perbedaan jumlah penyewaan sepeda yang cukup signifikan pada saat bukan hari kerja (saat libur / Holiday, hari Sabtu, dan Minggu) dibandingkan dengan hari kerja, yakni terdapat kenaikan 2 kali lipat lebih penyewaan sepeda pada hari kerja
        - Jumlah penyewaan sepeda tahun 2011 pada bukan hari kerja adalah 386839, dan naik menjadi 856264 pada hari kerja
        - Sedangkan tahun 2012 penyewaan sepeda berjumlah 613430 pada bukan hari kerja, dan meningkat menjadi 1436146 pada hari kerja
        
        **Conclusion pertanyaan 2 :**
        Terdapat perbedaan signifikan jumlah penyewaan sepeda pada hari bukan kerja dibandingkan pada hari kerja. Sehingga sangat direkomendasikan bagi penyewa sepeda yang ingin bepergian untuk memerhatikan apakah hari ini termasuk hari kerja atau bukan, dan bagi penyedia jasa layanan penyewaan sepeda agar dapat menjaga ketersediaan jumlah sepeda yang bisa untuk disewakan. Karena jumlah penyewaan sepeda pada hari kerja jauh lebih banyak dengan selisih 2,8 kali lipat pada 2011 dan 2 kali lipat pada 2012
        """
    )

def panggil_pertanyaan_3():
    st.subheader("Bagaimana cuaca memengaruhi jumlah penyewaan sepeda?", divider="red")

    def weathersit_conv(x):
        if x == 1:
            return "Clear"
        elif x == 2:
            return "Mist Cloudy"
        elif x == 3:
            return "Light Rain/Snow"
        elif x == 4:
            return "Heavy Rain/Snow\nThunderstorm"


    cnt_per_yr_weathersit = day_df.groupby(by=['yr','weathersit']).agg({
        'cnt': 'sum',
    }).reset_index()

    cnt_per_yr_weathersit.loc[len(cnt_per_yr_weathersit.index)] = [2011, 4, 0]
    cnt_per_yr_weathersit.loc[len(cnt_per_yr_weathersit.index)] = [2012, 4, 0]

    cnt_per_yr_weathersit["weathersit_str"] = cnt_per_yr_weathersit["weathersit"].apply(weathersit_conv)

    g = sns.catplot(
        data=cnt_per_yr_weathersit, kind="bar",
        x="weathersit_str", y="cnt", hue="yr", palette="Set1", height=10
    )
    for ax in g.axes.ravel():
        for c in ax.containers:
            ax.bar_label(c, label_type='edge', fmt = '%d')

    plt.title("Count of Bikes Rented on Weathersit in 2011 & 2012")
    plt.xlabel("Weathersits")
    plt.ylabel("Count of bikes rented")
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(plt.gcf())

    st.caption(
        """
        **Insight**
        - Grafik di atas memberikan informasi kepada kita bahwa cuaca sangat berpengaruh kepada jumlah penyewaan sepeda, dimana saat cuaca sedang baik (Clear), penyewaan sepeda menunjukkan jumlah terbanyak, baik tahun 2011 maupun 2012
        - Kemudian jumlah penyewaan tersebut menurun seiring dengan perubahan cuaca yang memburuk, hingga pada akhirnya saat terjadi cuaca ekstrem (Heavy Rain/Snow/Thunderstorm) tidak ada sama sekali orang yang menyewa sepeda untuk beraktivitas
        - Menariknya dari grafik di atas adalah saat cuaca sedang turun hujan/salju ringan, pada tahun 2011 menunjukkan jumlah yang lebih banyak daripada 2012 dengan selisih sekitar 2 kali lipat. Padahal seperti yang terdapat pada dataset ini, secara umum jumlah penyewaan sepeda tahun 2012 lebih banyak daripada tahun 2011
        
        **Conclusion pertanyaan 3 :**
        Keadaan cuaca yang baik juga sangat berpengaruh kepada jumlah penyewaan sepeda, dimana semakin baik cuacanya juga semakin banyak jumlah sepeda yang disewakan. Begitu juga saat cuaca buruk, jumlah penyewaan sepeda menjadi semakin sedikit dan turun drastis saat cuaca Light Rain/Snow hingga tidak ada orang yang menyewa sepeda saat cuaca ekstrem. Keadaan ini tentu saja bisa terjadi saat orang-orang mempertimbangkan keselamatan berdasarkan keadaan cuaca pada hari tersebut
        """
    )

def panggil_pertanyaan_4():
    st.subheader("Pada jam-jam berapa saja penyewaan sepeda terjadi paling banyak dan paling sedikit?", divider="red")

    cnt_per_yr_hr = hour_df.groupby(by=['yr','hr']).agg({
        'cnt': 'sum',
    }).reset_index()

    g = sns.catplot(
        data=cnt_per_yr_hr, kind="bar", orient="h",
        x="cnt", y="hr", hue="yr", palette="Set1", height=10,
    )
    for ax in g.axes.ravel():
        for c in ax.containers:
            ax.bar_label(c, label_type='edge', fmt = '%d')

    plt.title("Hourly Count of Bikes Rented in 2011 & 2012\n")
    plt.xlabel("Count of bikes rented")
    plt.ylabel("Hours")
    st.pyplot(plt.gcf())

    st.caption(
        """
        **Insight**
        - Grafik di atas memberikan informasi bahwa rentang pukul 0-5 adalah waktu dimana penyewaan sepeda paling sedikit terjadi pada tahun 2011 dan 2012. Hal ini menunjukkan bahwa rentang waktu tersebut mayoritas orang-orang sedang tidak melakukan aktivitas, atau bisa kita katakan waktu tersebut adalah normalnya waktu dimana orang-orang sedang beristirahat di rumah mereka masing-masing
        - Kemudian jumlah penyewaan sepeda di pagi hari meningkat pada pukul 6, dan naik signifikan pada pukul 7 dan 8. Hal tersebut bisa disimpulkan bahwa pada pukul 7 dan 8 pagi adalah waktu orang-orang mulai melakukan aktivitas di luar rumah seperti berangkat kerja, sekolah, kuliah, dan sebagainya dengan menyewa sepeda
        - Lalu pada sore hari, pukul 17 dan 18 adalah waktu dimana penyewaan sepeda paling banyak dalam sehari. Data ini mengisyaratkan bahwa pada waktu tersebut orang-orang sudah mulai pulang bekerja, sekolah, kuliah, dan aktivitas lainnya
        - Dan akhirnya jumlah penyewaan sepeda harian semakin menurun seiring semakin larutnya hari
        
        **Conclusion pertanyaan 4 :**
        Sangat disarankan kepada pengguna layanan penyewaan sepeda agar dapat memerhatikan waktu-waktu untuk menyewa sepeda, khususnya saat ingin mulai beraktivitas di pagi hari dan saat akan pulang di sore hari, dikarenakan jumlah penyewaan sepeda yang melonjak pada waktu-waktu tersebut. Hal ini bisa disiasati dengan melakukan booking lebih awal dengan mengatur waktu kapan akan menggunakan sepeda. Misalnya di pagi hari jika ingin menggunakan sepeda pada pukul 7, maka lebih baik melakukan booking sewa pada pukul 5 atau 6 pagi. Begitu juga pada sore hari
        """
    )

option = st.selectbox(
    "Analisis Data",
    ("Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4"),
    index=None,
    placeholder="Silakan Pilih...",
)

if option == "Pertanyaan 1":
    panggil_pertanyaan_1()
elif option == "Pertanyaan 2":
    panggil_pertanyaan_2()
elif option == "Pertanyaan 3":
    panggil_pertanyaan_3()
elif option == "Pertanyaan 4":
    panggil_pertanyaan_4()
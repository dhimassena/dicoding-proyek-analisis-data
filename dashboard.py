
import streamlit as st
import altair as alt
import os
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

# 1-----------------------------------------------------------------------------

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

# 2-----------------------------------------------------------------------------

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

plt.title("Count of Bikes Rented According to Workingday or Not in 2011 & 2012")
plt.xlabel("Kind of Days")
plt.ylabel("Count of bikes rented")
plt.ticklabel_format(style='plain', axis='y')

# 3-----------------------------------------------------------------------------

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

# 4-----------------------------------------------------------------------------

st.subheader("Pada jam-jam berapa saja penyewaan sepeda terjadi paling banyak dan paling sedikit?", divider="red")

cnt_per_yr_hr = hour_df.groupby(by=['yr','hr']).agg({
    'cnt': 'sum',
}).reset_index()

g = sns.catplot(
    data=cnt_per_yr_hr, kind="bar",
    x="hr", y="cnt", hue="yr", palette="Set1", height=10, aspect=1.5,
)
for ax in g.axes.ravel():
    for c in ax.containers:
        ax.bar_label(c, label_type='edge', fmt = '%d', rotation=75)

plt.title("Hourly Count of Bikes Rented in 2011 & 2012")
plt.xlabel("Hours")
plt.ylabel("Count of bikes rented")
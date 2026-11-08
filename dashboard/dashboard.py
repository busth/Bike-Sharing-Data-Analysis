
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi dashboard
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Membaca data
df = pd.read_csv("main_data.csv")

# Label data
df["jenis_hari"] = df["workingday"].map({
    0: "Hari Nonkerja",
    1: "Hari Kerja"
})

df["kondisi_cuaca"] = df["weathersit"].map({
    1: "Clear",
    2: "Mist + Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
})

df["tahun"] = df["yr"].map({
    0: "2011",
    1: "2012"
})

# Judul
st.title("🚲 Bike Sharing Dashboard 🚲", text_alignment="center")
st.space(size="medium")

# Sidebar
with st.sidebar:
    st.title("🚲 Bike Sharing 🚲", text_alignment="center")
    st.space(size="large")
    st.subheader("Filter Data")
    tahun = st.multiselect(
        "Pilih Tahun",
        options=["2011", "2012"],
        default=["2011", "2012"]
    )

    if not tahun:
        st.warning("Pilih minimal satu tahun.")
        st.stop()

    data = df[df["tahun"].isin(tahun)]

# Ringkasan
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Penyewaan",
    f"{data['cnt'].sum():,.0f}"
)

col2.metric(
    "Rata-rata Penyewaan",
    f"{data['cnt'].mean():.2f}"
)

jam_puncak = data.groupby("hr")["cnt"].mean().idxmax()

col3.metric(
    "Jam Puncak",
    f"{jam_puncak:02d}:00"
)

st.divider()

# Grafik 1: Penyewaan berdasarkan jam dan jenis hari
st.subheader("1. Penyewaan Berdasarkan Jam dan Jenis Hari")

hourly = (
    data.groupby(["workingday", "hr"])["cnt"]
    .mean()
    .reset_index()
)

hourly["jenis_hari"] = hourly["workingday"].map({
    0: "Hari Nonkerja",
    1: "Hari Kerja"
})

fig, ax = plt.subplots(figsize=(10, 5))

sns.lineplot(
    data=hourly,
    x="hr",
    y="cnt",
    hue="jenis_hari",
    marker="o",
    ax=ax
)

peak = hourly.loc[
    hourly.groupby("workingday")["cnt"].idxmax()
]

for _, row in peak.iterrows():
    ax.annotate(
        f"{row['cnt']:.2f}",
        xy=(row["hr"], row["cnt"]),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        fontsize=10
    )

ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks(range(24))
ax.grid(alpha=0.3)
ax.margins(y=0.15)

st.pyplot(fig)
plt.close(fig)

# Insight grafik 1
peak = hourly.loc[
    hourly.groupby("workingday")["cnt"].idxmax()
]

for _, row in peak.iterrows():
    st.write(
        f"- {row['jenis_hari']} mencapai puncak "
        f"pukul {int(row['hr']):02d}:00 dengan rata-rata "
        f"{row['cnt']:.2f} penyewaan."
    )

st.divider()

# Grafik 2: Penyewaan berdasarkan cuaca
st.subheader("2. Penyewaan Berdasarkan Kondisi Cuaca")

weather = (
    data.groupby("kondisi_cuaca")["cnt"]
    .agg(["mean", "count"])
    .reset_index()
    .sort_values("mean", ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=weather,
    x="kondisi_cuaca",
    y="mean",
    hue="kondisi_cuaca",
    legend=False,
    ax=ax
)

ax.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
ax.margins(y=0.15)

for i, row in weather.reset_index(drop=True).iterrows():
    ax.text(
        i,
        row["mean"] + 2,
        f"{row['mean']:.2f}\n(n={row['count']})",
        ha="center"
    )

st.pyplot(fig)
plt.close(fig)

# Insight grafik 2
st.write(
    f"- Penyewaan tertinggi terjadi pada cuaca "
    f"{weather.iloc[0]['kondisi_cuaca']} dengan rata-rata "
    f"{weather.iloc[0]['mean']:.2f}."
)

st.write(
    f"- Penyewaan terendah terjadi pada cuaca "
    f"{weather.iloc[-1]['kondisi_cuaca']} dengan rata-rata "
    f"{weather.iloc[-1]['mean']:.2f}."
)

st.info(
    "Catatan: Kategori Heavy Rain/Snow hanya memiliki "
    "sedikit pengamatan sehingga hasilnya perlu "
    "ditafsirkan secara hati-hati."
)

st.divider()

st.caption(
    "Bike Sharing Dashboard (2011–2012). by: Ngali Busthomi", text_alignment="center"
)

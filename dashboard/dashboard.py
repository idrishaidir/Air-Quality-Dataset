import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

changping_df = pd.read_csv('data/changping.csv')

changping_df["Tanggal"] = pd.to_datetime(changping_df["Tanggal"], errors="coerce")

changping_df["Tahun"] = changping_df["Tanggal"].dt.year
changping_df["Bulan"] = changping_df["Tanggal"].dt.month
changping_df["Hari"] = changping_df["Tanggal"].dt.day

st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", changping_df["Tanggal"].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", changping_df["Tanggal"].max().date())

filtered_df = changping_df[
    (changping_df["Tanggal"] >= pd.to_datetime(start_date)) & 
    (changping_df["Tanggal"] <= pd.to_datetime(end_date))
]

selected_pollutant = st.sidebar.selectbox("Pilih Polutan", ["PM2.5", "PM10", "NO2", "All"])

waktu = st.sidebar.selectbox("waktu", ["Tahun", "Bulan", "Hari"])

if waktu == "Tahun":
    filtered_df = filtered_df.groupby("Tahun")[[selected_pollutant] if selected_pollutant != "All" else ['PM2.5', 'PM10', 'NO2']].mean().reset_index()
    x_label = "Tahun"
elif waktu == "Bulan":
    filtered_df = filtered_df.groupby(["Tahun", "Bulan"])[[selected_pollutant] if selected_pollutant != "All" else ['PM2.5', 'PM10', 'NO2']].mean().reset_index()
    filtered_df["Periode"] = filtered_df["Tahun"].astype(str) + "-" + filtered_df["Bulan"].astype(str)
    x_label = "Periode"
elif waktu == "Hari":
    filtered_df = filtered_df.groupby(["Tahun", "Bulan", "Hari"])[[selected_pollutant] if selected_pollutant != "All" else ['PM2.5', 'PM10', 'NO2']].mean().reset_index()
    filtered_df["Periode"] = filtered_df["Tahun"].astype(str) + "-" + filtered_df["Bulan"].astype(str) + "-" + filtered_df["Hari"].astype(str)
    x_label = "Periode"

st.title("Air Quality Dashboard")
st.header(f"Tren {selected_pollutant if selected_pollutant != 'All' else 'SEMUA POLUTAN'} berdasarkan {waktu}")

fig1, ax1 = plt.subplots(figsize=(10, 5))
if selected_pollutant == "All":
    for col in ['PM2.5', 'PM10', 'NO2']:
        sns.lineplot(x=filtered_df[x_label], y=filtered_df[col], marker="o", label=col, ax=ax1)
    ax1.legend(title="Polutan")
else:
    sns.lineplot(x=filtered_df[x_label], y=filtered_df[selected_pollutant], marker="o", ax=ax1)

ax1.set_xlabel(waktu)
ax1.set_ylabel(f"Kadar Rata-rata {selected_pollutant if selected_pollutant != 'All' else 'PM2.5, PM10, NO2'}")
ax1.set_title(f"Tren {selected_pollutant if selected_pollutant != 'All' else 'PM2.5, PM10, NO2'} berdasarkan {waktu}")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.header("Korelasi antara Suhu dan Polutan")
corr_temp = changping_df[["TEMP", "PM2.5", "PM10", "NO2"]].corr()
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_temp, annot=True, cmap="coolwarm", fmt=".2f", ax=ax2)
ax2.set_title("Korelasi antara Suhu dan Polutan")
st.pyplot(fig2)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Functions (Updated 'musim' function name and aggregation method)
def season_df(day_df):
    season_df = day_df.groupby(by="season").count().reset_index()
    return season_df

# Load data
day_df = pd.read_csv("all_data.csv")

# Sidebar
with st.sidebar:
    st.image("bike_logo.jpg", use_column_width=True)
    min_date = pd.to_datetime(day_df["dateday"].min()) # Convert to datetime
    max_date = pd.to_datetime(day_df["dateday"].max())  # Convert to datetime
    start_date = st.date_input(label="Start Date", value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input(label="End Date", value=max_date, min_value=min_date, max_value=max_date)

# Filter data based on selected dates
main_df_days = day_df[(day_df["dateday"] >= str(start_date)) & (day_df["dateday"] <= str(end_date))]

# Additional data processing (total_registered_df, total_casual_df)

# Dashboard
st.header('Dicoding Assignment: Analisa Dataset Bike Sharing :sparkles:')
st.subheader('Daily Sharing')

col1, col2, col3 = st.columns(3)
 
with col1:
    total_sharing = main_df_days['count'].sum()
    st.metric("Total Sharing Bike", value=total_sharing)

with col2:
    total_sum_casual = day_df.casual.sum()
    st.metric("Total Casual", value=total_sum_casual)

with col3:
    total_sum_regis = day_df.casual.sum()
    st.metric("Total Casual", value=total_sum_regis)

# Visualizations
# Season analysis
season_data = season_df(main_df_days)
st.subheader("Seasonal Analysis")
st.write(season_data)

# Weather analysis
user_per_weather = day_df.groupby("weather").agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
}).reset_index()
st.subheader("Weather Impact")
st.write(user_per_weather)

# Season Analysis
user_per_season = day_df.groupby("season").agg({
    "casual": "sum",
    "registered": "sum",
    "count": "sum"
}).reset_index()
st.subheader("Season Impact")
st.write(user_per_season)


# Plotting with Streamlit's native capabilities
st.subheader("Weather Impact Visualization")
st.bar_chart(user_per_weather.set_index("weather"))

# Performa 2 Tahun Terakhir
st.subheader("1. Bagaimana Performa Peminjaman Sepeda Dari 2 Tahun Terakhir?")
daily_counts = main_df_days.groupby('dateday')['count'].sum()  # Calculate daily counts
st.line_chart(daily_counts, use_container_width=True)

# Kondisi Weather Terhadap Peminjaman Sepeda
st.subheader("2. Bagaimana Kondisi Weather/Cuaca Dapat Mempengaruhi Jumlah Peminjaman Sepeda Pada Casual & Registered User?")
st.bar_chart(user_per_weather.set_index("weather"))

# Pengaruh Variabel Season Terhadap Peminjaman Sepeda
st.subheader("3. Apakah variabel season mempengaruhi jumlah peminjaman sepeda pada Casual & Registered User?")
st.bar_chart(user_per_season.set_index("season"))

# Grafik Pie Chart Antara Casual & Registred User Dengan Season
st.subheader("4. Manakah peminjam terbanyak setiap musim? Pada musim apa mereka banyak meminjam sepeda?")
# Menentukan Warna Yang Akan Dipakai Pada Grafik
colors = ["#D3D3D3", "#FBA834"]

# Mengelompokkan DataFrame berdasarkan Season dan Menjumlahkan Kolom Registered & Casual
seasonal_users = day_df.groupby('season')[['casual', 'registered']].sum()

# Membuat Pie Chart Untuk Setiap Musim
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()

# Melakukan Looping Pada Setiap Musim & Menggambarkan Pie Chart
for i, (season, data) in enumerate(seasonal_users.iterrows()):
    ax = axes[i]
    ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.set_title(f"Season {season}")

# Menampilkan Pie Chart
st.pyplot(fig)
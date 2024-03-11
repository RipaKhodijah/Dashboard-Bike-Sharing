import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime
from PIL import Image
import os

# Set tema untuk dark mode
st.set_page_config(page_title="Bike Sharing", page_icon="🚲", layout="wide")
st.markdown("""
    <style>
        body {
            color: white;
            background-color: #1E1E1E;
        }
        .st-dg, .st-c9 {
            color: white;
        }
        .st-ew {
            background-color: #1E1E1E;
        }
        .st-fx, .st-en, .st-eo, .st-eh, .st-ex, .st-fy {
            background-color: transparent;
        }
    </style>
""", unsafe_allow_html=True)

# Direktori
script_directory = os.path.dirname(os.path.abspath(__file__))

# Relative Path
data_path = os.path.join(script_directory, 'Data_Hasil_Analisis.csv')
image_path = os.path.join(script_directory, 'sepeda.jpg')

# Membaca data dari file CSV
filtered_data = pd.read_csv(data_path)

# menampilkan logo
img = Image.open(image_path)
st.sidebar.image(img)
st.title('Bike Sharing 🚲🚲')

# Mengambil sampel data
sampled_data = filtered_data.sample(n=min(500, len(filtered_data)))

# Menampilkan kalender untuk memilih rentang tanggal
st.sidebar.header('Rentang Waktu')
start_date = st.sidebar.date_input("Mulai", min_value=pd.to_datetime(filtered_data['instant']).min().date(),
                                   max_value=pd.to_datetime(filtered_data['instant']).max().date(),
                                   value=pd.to_datetime(filtered_data['instant']).min().date())
end_date = st.sidebar.date_input("Selesai", min_value=pd.to_datetime(filtered_data['instant']).min().date(),
                                 max_value=pd.to_datetime(filtered_data['instant']).max().date(),
                                 value=pd.to_datetime(filtered_data['instant']).max().date())

# Konversi tipe data date menjadi datetime64[ns]
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = filtered_data[(pd.to_datetime(filtered_data['instant']).dt.date >= start_date.date()) &
                              (pd.to_datetime(filtered_data['instant']).dt.date <= end_date.date())]

# Menampilkan plot suhu menggunakan Plotly
st.subheader("Plot of Temperature")

# Membuat subplot untuk tiga kolom pertama
fields = ['temp', 'atemp', 'hum', 'windspeed']
fields = fields[:3]  

fig = make_subplots(rows=len(fields), cols=1, subplot_titles=fields)

for i, f1 in enumerate(fields):
    fig.add_trace(go.Scatter(x=filtered_data['instant'], y=filtered_data[f1], mode='markers', name=f1),
                  row=i+1, col=1)

fig.update_layout(title_text='Temperature Over Time', xaxis_title='Date', yaxis_title='Temperature (°C)')
st.plotly_chart(fig)

# Menampilkan plot bar chart untuk kolom 'cnt' yang dipilih
selected_column = st.sidebar.selectbox("Pilih kolom untuk ditampilkan", filtered_data.columns)
if selected_column != 'instant':
    st.subheader(f"Bar Chart of 'cnt' by '{selected_column}'")
    fig = px.bar(filtered_data, x=selected_column, y='cnt', color=selected_column,
                 title=f'Count of Bikes by {selected_column}')
    st.plotly_chart(fig)

# Menampilkan plot distribusi untuk kolom 'cnt'
st.subheader("Distribution Plot of 'cnt'")
fig, ax = plt.subplots(figsize=(6, 4)) 
sns.histplot(filtered_data['cnt'], bins=50, color='darkblue')
st.pyplot(fig)

# Menampilkan heatmap of correlation
st.subheader("Heatmap of Correlation")
fig, ax = plt.subplots(figsize=(10, 5))  
sns.heatmap(filtered_data.corr(method='pearson'))  
st.pyplot(fig)

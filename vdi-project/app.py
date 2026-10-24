import streamlit as st
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Multi-DBMS E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# Tentukan path absolut direktori proyek
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "database", "ecommerce_local.db")

# --- 1. FUNGSI DATA PIPELINE (PENGAMBILAN & PENGGABUNGAN DATA) ---
@st.cache_data
def load_and_merge_data():
    # Ambil data dari DBMS 1 (SQLite - Data Produk)
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    df_products = pd.read_sql("SELECT * FROM products", sqlite_conn)
    sqlite_conn.close()
    
    # Ambil data dari DBMS 2 (PostgreSQL / Supabase - Data Transaksi)
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        try:
            db_url = st.secrets["SUPABASE_DB_URL"]
        except Exception:
            pass
            
    if not db_url:
        raise ValueError("URL Database PostgreSQL tidak ditemukan di .env maupun st.secrets!")
        
    engine = create_engine(db_url)
    df_transactions = pd.read_sql("SELECT * FROM transactions", engine)
    
    # DATA PIPELINE / FEDERATION: Gabungkan tabel dari SQLite dan PostgreSQL via Pandas merge
    df_merged = pd.merge(df_transactions, df_products, on="product_id", how="inner")
    
    # Hitung total pendapatan (Revenue)
    df_merged['total_revenue'] = df_merged['quantity'] * df_merged['unit_price']
    
    return df_merged

# Eksekusi pipeline
try:
    df = load_and_merge_data()
except Exception as e:
    st.error(f"Gagal terhubung ke Database: {e}")
    st.stop()

# --- 2. ANTARMUKA VISUALISASI WEB (STREAMLIT) ---
st.title("📊 Dashboard Analitik Multi-DBMS: E-Commerce")
st.markdown("Aplikasi web interaktif ini mengintegrasikan **SQLite (Lokal)** untuk Data Master Produk dan **PostgreSQL (Cloud Supabase)** untuk Data Transaksi[cite: 1].")

# Sidebar Filter Interaktif
st.sidebar.header("🎛️ Filter Interaktif")
selected_region = st.sidebar.multiselect(
    "Pilih Wilayah (Region):",
    options=df["region"].unique(),
    default=df["region"].unique()
)

df_filtered = df[df["region"].isin(selected_region)]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pendapatan", f"Rp {df_filtered['total_revenue'].sum():,.0f}")
with col2:
    st.metric("Total Produk Terjual", int(df_filtered['quantity'].sum()))
with col3:
    st.metric("Jumlah Transaksi", len(df_filtered))

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📈 Pendapatan Berdasarkan Kategori Produk")
    category_revenue = df_filtered.groupby("category")["total_revenue"].sum().reset_index()
    fig_cat = px.bar(
        category_revenue, x="category", y="total_revenue",
        color="category", text_auto=".2s",
        labels={"category": "Kategori", "total_revenue": "Total Pendapatan (Rp)"}
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b:
    st.subheader("🌍 Distribusi Penjualan per Wilayah")
    region_sales = df_filtered.groupby("region")["total_revenue"].sum().reset_index()
    fig_reg = px.pie(
        region_sales, names="region", values="total_revenue", hole=0.4,
        labels={"region": "Wilayah", "total_revenue": "Pendapatan"}
    )
    st.plotly_chart(fig_reg, use_container_width=True)

st.subheader("📑 Tabel Data Hasil Integrasi (SQLite + PostgreSQL)")
st.dataframe(df_filtered, use_container_width=True)
""")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os
sns.set(style='dark')


# Load Data
@st.cache_data
def load_data():
    def get_file_path(filename):
        return f"dashboard/{filename}" if os.path.exists(f"dashboard/{filename}") else filename
    
    customers_df = pd.read_csv(get_file_path("customers_dataset.csv"))
    order_items_df = pd.read_csv(get_file_path("order_items_dataset.csv"))
    order_product_english_df = pd.read_csv(get_file_path("order_product_english_df.csv"))
    order_payments_df = pd.read_csv(get_file_path("order_payments_dataset.csv"))
    order_reviews_df = pd.read_csv(get_file_path("order_reviews_dataset.csv"))
    orders_dataset_df = pd.read_csv(get_file_path("orders_dataset.csv"))
    rfm_df = pd.read_csv(get_file_path("rfm_df.csv"))
    
    return (customers_df, order_items_df, order_product_english_df, 
            order_payments_df, order_reviews_df, orders_dataset_df, rfm_df)

(customers_df, order_items_df, order_product_english_df, 
 order_payments_df, order_reviews_df, orders_dataset_df, rfm_df) = load_data()

# Show the current working directory
# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def top_cities(df, n=10):
    return df.groupby("customer_city")["customer_id"].nunique().sort_values(ascending=False).head(n)

def compute_sales_trend(df):
    if "order_purchase_timestamp" in df.columns:
        df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors='coerce')
        df = df.dropna(subset=["order_purchase_timestamp"])
        return df.set_index("order_purchase_timestamp").resample("ME").size()
    else:
        st.error("Missing 'order_purchase_timestamp' column")
        return pd.Series()

def create_penjual_terbanyak(df):
    penjual_terbanyak = df.groupby("seller_id")["order_id"].nunique().sort_values(ascending=False)

    return penjual_terbanyak

def create_top_categories(df):
    top_categories = df.groupby("product_category_name_english")["order_id"].count().sort_values(ascending=False)
    
    return top_categories
def create_top_revenue(df):
    top_revenue = df.groupby(by="product_category_name_english").agg({
    "price":"sum"}).sort_values(by="price", ascending=False) 
    
    return top_revenue

def payment (df):
    payment_counts = df["payment_type"].value_counts()
    return payment_counts

def review (df):
    review=df["review_score"].value_counts().sort_index()
    return review
def orders_trend(df):
    # Mengonversi tanggal pada dataset orders
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

    # Membuat agregasi jumlah pesanan per bulan
    orders_trend = df.set_index("order_purchase_timestamp").resample("ME").size()
    return orders_trend

def Waktu_Pengiriman(df):
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["range_time"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days   
    
    return df["range_time"] 


# # Menyiapkan berbagai dataframe
persebaran_customer = top_cities(customers_df)
penjualan_terbanyak = create_penjual_terbanyak(order_items_df)
top_categories = create_top_categories(order_product_english_df)
top_revenue = create_top_revenue(order_product_english_df)
payment_df = payment(order_payments_df)
review = review(order_reviews_df)
orders_trend = orders_trend(orders_dataset_df)
Distribusi = Waktu_Pengiriman(orders_dataset_df)
rfm_df = rfm_df


# plot number of daily orders (2021)
st.header('Fariz Submission Dashboard :sparkles:')
st.subheader('Daily Orders')

#Kota persebaran customer dan Penjualan seller terbanyak


st.sidebar.header("Filter Data")
num_cities = st.sidebar.slider("Jumlah Kota Teratas", min_value=5, max_value=20, value=10)
num_categories = st.sidebar.slider("Jumlah Kategori Teratas", min_value=5, max_value=20, value=10)


st.subheader("Top Kota dengan Jumlah Pelanggan Terbanyak")
city_data = top_cities(customers_df, n=num_cities)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=city_data.index, y=city_data.values, palette="Blues_r", ax=ax)
ax.set_xlabel("Kota")
ax.set_ylabel("Jumlah Pelanggan")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)


st.subheader("Tren Jumlah Pesanan per Bulan")
sales_trend_data = compute_sales_trend(orders_dataset_df)
if not sales_trend_data.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sales_trend_data.plot(marker="o", linestyle="-", color="b", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Pesanan")
    st.pyplot(fig)
else:
    st.warning("No data available for sales trend.")

st.subheader("Kategori Produk Terlaris")
top_categories = order_product_english_df.groupby("product_category_name_english")["order_id"].count().sort_values(ascending=False).head(num_categories)
fig, ax = plt.subplots(figsize=(12, 6))
top_categories.plot(kind="barh", color="green", ax=ax)
ax.set_title("Kategori Produk Terlaris")
ax.set_xlabel("Jumlah Produk Terjual")
ax.set_ylabel("Kategori Produk")
ax.grid(axis="x")
st.pyplot(fig)

st.subheader("Kategori Produk Revenue Tertinggi")
top_revenue = order_product_english_df.groupby("product_category_name_english").agg({"price":"sum"}).sort_values(by="price", ascending=False).head(num_categories)
fig, ax = plt.subplots(figsize=(12, 6))
top_revenue.plot(kind="barh", color="green", ax=ax)
ax.set_title("Kategori Produk Revenue Tertinggi")
ax.set_xlabel("Jumlah Revenue Produk Terjual")
ax.set_ylabel("Kategori Produk")
ax.grid(axis="x")
st.pyplot(fig)

# Payment Methods Distribution
st.subheader("Distribusi Metode Pembayaran")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=payment_df.index, y=payment_df.values, palette="coolwarm")
ax.set_xlabel("Metode Pemabayaran")
ax.set_ylabel("Jumlah Transaksi")
st.pyplot(fig)

# Review Score Distribution
st.subheader("Distribusi Skor Ulasan")
fig, ax = plt.subplots(figsize=(8, 6))
review.plot(kind="bar", color="purple", ax=ax)
ax.set_xlabel("Rating Review")
ax.set_ylabel("Score Review")
st.pyplot(fig)

# Delivery Time Distribution
st.subheader("Distribusi Waktu Pengiriman")
fig, ax = plt.subplots(figsize=(8, 6))
sns.histplot(Distribusi, bins=30, kde=True, color="blue", alpha=0.5)
ax.set_xlabel("Hari Order Hingga Diterima")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

#RFM
st.subheader("RFM Distribution")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

# Warna untuk setiap grafik
colors = ["#72BCD4"] * 5

# Plot Recency (Pelanggan dengan waktu transaksi terbaru)
sns.barplot(y="Recency", x="customer_id", 
            data=rfm_df.sort_values(by="Recency", ascending=True).head(5), 
            palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15, rotation=90)

# Plot Frequency (Pelanggan dengan transaksi terbanyak)
sns.barplot(y="Frequency", x="customer_id", 
            data=rfm_df.sort_values(by="Frequency", ascending=False).head(5), 
            palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15, rotation=90)

# Plot Monetary (Pelanggan dengan total pengeluaran tertinggi)
sns.barplot(y="Monetary", x="customer_id", 
            data=rfm_df.sort_values(by="Monetary", ascending=False).head(5), 
            palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15, rotation=90)

st.pyplot(fig)

st.caption('Copyright © Muhammad Fariz Ramadhan 2025')

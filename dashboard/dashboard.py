import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def persebaran_customer(df):
    persebaran_customer = customers_df.groupby("customer_city")["customer_id"].nunique().sort_values( ascending=False)

    return persebaran_customer

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
# Load cleaned data
customers_df = pd.read_csv("./customers_dataset.csv")
order_items_df = pd.read_csv("./order_items_dataset.csv")
order_product_english_df = pd.read_csv("./order_product_english_df.csv")
order_payments_df = pd.read_csv("./order_payments_dataset.csv")
order_reviews_df = pd.read_csv("./order_reviews_dataset.csv")
orders_dataset_df = pd.read_csv("./orders_dataset.csv")
rfm_df = pd.read_csv("./rfm_df.csv")



# # Menyiapkan berbagai dataframe
persebaran_customer = persebaran_customer(customers_df)
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
st.subheader('Kota Persebaran Customer dan Penjual')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Plot persebaran pelanggan
sns.barplot(x=persebaran_customer.head(10).index, 
            y=persebaran_customer.head(10).values, 
            ax=ax[0], 
            palette="Blues_r")

ax[0].set_title("10 Kota dengan Jumlah Pelanggan Terbanyak", fontsize=30)
ax[0].set_xlabel("Kota", fontsize=30)
ax[0].set_ylabel("Jumlah Pelanggan", fontsize=30)
ax[0].tick_params(axis='x', rotation=75, labelsize=35)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].grid(axis="y")

# Plot penjualan terbanyak
sns.barplot(x=penjualan_terbanyak.head(10).index, 
            y=penjualan_terbanyak.head(10).values, 
            ax=ax[1], 
            palette="Blues_r")

ax[1].set_title("10 ID Seller dengan Jumlah Order Terbanyak", fontsize=30)
ax[1].set_xlabel("ID Seller", fontsize=30)
ax[1].set_ylabel("Jumlah Order", fontsize=30)
ax[1].tick_params(axis='x', rotation=90, labelsize=35)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].grid(axis="y")

st.pyplot(fig)

    

# Daily Orders Trend
st.subheader('Tren Jumlah Pesanan')
fig, ax = plt.subplots(figsize=(12, 6))
orders_trend.plot(marker="o", linestyle="-", color="b", ax=ax)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pesanan")
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

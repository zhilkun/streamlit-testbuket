import streamlit as st
import pandas as pd
import os

# Judul
st.title("💐 Buket AI")
st.write("Masukkan preferensi kamu, dan sistem akan merekomendasikan buket yang cocok!")

# Input user
budget = st.number_input("💰 Budget maksimal (Rp)", min_value=50000, step=50000, value=200000)
warna = st.selectbox("🎨 Warna favorit buket:", ["merah", "biru", "kuning", "hijau", "ungu", "putih"])
acara = st.text_input("🎉 Untuk acara apa? (contoh: ulang tahun, wisuda, anniversary)", "wisuda")

# Baca data dari CSV
try:
    df = pd.read_csv("buket.csv")
except FileNotFoundError:
    st.error("⚠️ File buket.csv tidak ditemukan. Pastikan ada di folder yang sama dengan buketai.py")
    st.stop()

# Convert DataFrame ke list of dict
buket_list = df.to_dict(orient="records")

# Tambahkan contoh acara default (biar matching lebih enak)
for b in buket_list:
    if "acara" not in b:
        # kasih default acara sesuai warna
        if b["warna"] == "merah":
            b["acara"] = "ulang tahun"
        elif b["warna"] == "kuning" or b["warna"] == "hijau":
            b["acara"] = "wisuda"
        else:
            b["acara"] = "anniversary"

# Tombol untuk mencari rekomendasi
if st.button("🔍 Cari Rekomendasi"):
    rekomendasi = [b for b in buket_list if b["harga"] <= budget and (b["warna"] == warna or b["acara"] == acara.lower())]

    if rekomendasi:
        st.subheader("✨ Rekomendasi Buket untuk Kamu")
        for b in rekomendasi:
            st.markdown(f"### {b['nama']}")
            st.write(f"💰 Harga: Rp{b['harga']}")
            st.write(f"📦 Stok: {b['stok']}")
            st.write(f"🎨 Warna: {b['warna']}")
            st.write(f"🎉 Cocok untuk acara: **{b['acara']}**")

            # Path gambar
            gambar_path = os.path.join("images", str(b["gambar"]))
            if os.path.exists(gambar_path):
                st.image(gambar_path, width=300)
            else:
                st.warning(f"Gambar tidak ditemukan: {b['gambar']}")

            st.markdown("---")
    else:
        st.warning("⚠️ Maaf, tidak ada buket yang sesuai dengan preferensi kamu.")

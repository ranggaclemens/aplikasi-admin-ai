import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- BAGIAN KONFIGURASI ---
# Tempel API Key Anda di antara tanda kutip di bawah ini

# Konfigurasi AI
# Mengambil kunci dari Brankas Rahasia Streamlit
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- TAMPILAN WEBSITE ---
st.set_page_config(page_title="AI Admin Otomatis", layout="wide")

st.title("🤖 AI Admin: Dari Chat Jadi Excel")
st.write("Copy chat pesanan yang berantakan, paste di bawah, biarkan AI merapikannya.")

# Kolom Input
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Paste Chat Disini")
    raw_text = st.text_area("Masukan teks pesanan (WhatsApp/Email):", height=300)
    process_btn = st.button("✨ Proses Data Sekarang", type="primary")

# --- LOGIKA OTAK AI ---
if process_btn and raw_text:
    with col2:
        st.subheader("2. Hasil Rapih (Excel)")
        with st.spinner("Sedang memanggil otak AI..."):
            try:
                # Perintah ke AI (Prompt Engineering)
                prompt = f"""
                Kamu adalah asisten admin admin. Tugasmu adalah mengekstrak data pesanan dari teks berikut.
                Teks: "{raw_text}"
                
                Instruksi:
                1. Identifikasi Nama Pelanggan, Alamat Kota, Barang Pesanan, Warna, Ukuran, Jumlah, dan Metode Bayar.
                2. Jika ada informasi yang tidak ada, isi dengan "-".
                3. Keluarkan HANYA dalam format JSON List. Jangan ada teks lain.
                
                Contoh format JSON:
                [
                    {{"Nama": "Budi", "Kota": "Jakarta", "Barang": "Kaos", "Warna": "Hitam", "Ukuran": "L", "Qty": 2, "Bayar": "Transfer"}}
                ]
                """
                
                # Mengirim ke Google
                response = model.generate_content(prompt)
                cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
                
                # Mengubah jadi Tabel
                data_json = json.loads(cleaned_text)
                df = pd.DataFrame(data_json)
                
                # Tampilkan Tabel
                st.dataframe(df, use_container_width=True)
                
                # Tombol Download Excel
                file_excel = "data_pesanan.xlsx"
                df.to_excel(file_excel, index=False)
                
                with open(file_excel, "rb") as file:
                    st.download_button(
                        label="📥 Download File Excel",
                        data=file,
                        file_name="rekap_pesanan.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                st.success("Berhasil! Data siap didownload.")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}. Coba cek API Key atau format teksnya.")

elif process_btn and not raw_text:
    st.warning("Tolong masukkan teks chatnya dulu ya.")

# Footer
st.markdown("---")
st.caption("Dibuat dengan Python & Gemini AI")
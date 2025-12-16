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

# --- TAMPILAN WEBSITE (VERSI BISNIS) ---
st.set_page_config(page_title="Jose AI Assistant", layout="wide")

# --- SIDEBAR (IDENTITAS BISNIS ANDA) ---
with st.sidebar:
    st.header("🏢 Jose AI Tools")
    st.info("Aplikasi ini dibuat khusus untuk membantu UMKM merekap orderan otomatis.")
    
    st.write("---")
    st.header("👤 Tentang Creator")
    st.write("**Jose Digital Solutions**")
    st.caption("Membantu UMKM kerja lebih cepat dengan Automasi AI.")
    
    # Tombol Link ke WhatsApp Anda (GANTI NOMOR INI!)
    wa_link = "https://wa.me/6285602683808?text=Halo%20saya%20tertarik%20bikin%20aplikasi%20AI"
    st.link_button("🚀 Pesan Aplikasi Ini", wa_link)

# --- BAGIAN UTAMA ---
st.title("🤖 Asisten Rekap Orderan Otomatis")
st.markdown("""
**Capek rekap chat satu-satu ke Excel?** Paste chat orderan yang berantakan di bawah, biarkan AI merapikannya dalam 1 detik.
""")

# Kolom Input dan Output
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Paste Chat Disini")
    chat_input = st.text_area("Masukan teks pesanan (WhatsApp/Email):", height=300, placeholder="Contoh: Mas Budi pesen Kaos Hitam L 2pcs kirim ke Jakarta...")
    tombol_proses = st.button("✨ Proses Data Sekarang", type="primary")

with col2:
    st.subheader("2. Hasil Rapih (Excel)")
    
    if tombol_proses and chat_input:
        with st.spinner("Sedang memproses... (Tunggu sebentar)"):
            try:
                # Prompt Rahasia (Instruksi ke Otak AI)
                prompt = f"""
                Kamu adalah admin toko online yang teliti. 
                Tugasmu adalah mengekstrak data pesanan dari teks berikut menjadi format JSON.
                Ambil data: Nama, Kota, Barang, Warna, Ukuran, Qty (jumlah), dan Cara Bayar.
                
                Teks pesanan:
                "{chat_input}"
                
                Keluarkannya HANYA JSON murni. Jangan ada tulisan lain.
                Format JSON list of objects: [{{...}}, {{...}}]
                """
                
                response = model.generate_content(prompt)
                cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(cleaned_response)
                
                # Buat Tabel
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                
                # Tombol Download
                excel_file = "rekap_order.xlsx"
                df.to_excel(excel_file, index=False)
                with open(excel_file, "rb") as f:
                    st.download_button("📥 Download File Excel", f, file_name="rekap_harian.xlsx")
                    
                st.success("Berhasil! Data siap didownload.")
                
            except Exception as e:
                st.error("Gagal memproses. Coba cek format teksnya atau coba lagi.")
                st.error(f"Error detail: {e}")

    elif not chat_input:
        st.info("👈 Silakan masukkan teks pesanan di sebelah kiri dulu.")
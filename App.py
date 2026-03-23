import streamlit as st
import json
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SceneCrafter AI", page_icon="🎬", layout="wide")

st.title("🎬 SceneCrafter AI")
st.markdown("Ubah satu ide menjadi naskah video panjang lengkap dengan prompt visual.")

# --- SETUP API GEMINI DARI STREAMLIT SECRETS ---
try:
    # Mengambil API Key dari pengaturan rahasia Streamlit
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Menggunakan model Flash yang cepat dan efisien
    model = genai.GenerativeModel('gemini-pro')
except KeyError:
    st.error("⚠️ API Key belum diatur! Silakan masukkan GEMINI_API_KEY di pengaturan rahasia (Secrets) Streamlit.")
    st.stop()

# --- SIDEBAR: INPUT PENGGUNA ---
with st.sidebar:
    st.header("⚙️ Pengaturan Video")
    ide_user = st.text_area("Ide Singkat", placeholder="Misal: Misteri hilangnya kapal Mary Celeste...")
    niche = st.selectbox("Niche/Tema", ["Misteri", "Edukasi", "Horor", "Islami", "Cerita Anak", "Bisnis"])
    durasi = st.selectbox("Target Durasi", ["5 Menit", "10 Menit", "20 Menit", "30 Menit"])
    rasio = st.selectbox("Aspek Rasio", ["16:9 (YouTube Horizontal)", "9:16 (Shorts/TikTok)"])
    tone = st.selectbox("Tone Suara", ["Dokumenter Tegang", "Santai & Edukatif", "Mencekam", "Inspiratif"])
    
    generate_btn = st.button("🚀 Generate Video Script", type="primary", use_container_width=True)

# --- MASTERPIECE SYSTEM PROMPT ---
def get_system_prompt(ide, niche, durasi, rasio, tone):
    return f"""
    Kamu adalah Cinematic Director & Master Scriptwriter AI.
    Tugasmu mengubah ide mentah menjadi naskah video terstruktur.
    
    INPUT DATA:
    - Ide: {ide}
    - Niche: {niche}
    - Durasi: {durasi}
    - Rasio: {rasio}
    - Tone: {tone}
    
    ATURAN:
    1. Hook 15 detik pertama harus memikat.
    2. Pacing: Bagi naskah menjadi scene pendek (15-30 detik).
    3. Visual Prompt: Tulis prompt gambar dalam bahasa Inggris yang detail sesuai rasio {rasio}.
    4. Narasi: Gunakan bahasa Indonesia sesuai tone {tone}.
    
    WAJIB OUTPUT DALAM FORMAT JSON BERIKUT TANPA TEKS LAIN, TANPA MARKDOWN (```json):
    {{
      "project_overview": {{
        "ide_utama": "...",
        "alternatif_judul": ["Judul 1", "Judul 2", "Judul 3"],
        "thumbnail_image_prompt": "English prompt..."
      }},
      "hook_pembuka": "...",
      "scenes": [
        {{
          "scene_number": 1,
          "estimated_duration": "15 detik",
          "visual_description": "...",
          "ai_image_prompt": "...",
          "narration_script": "..."
        }}
      ]
    }}
    """

# --- LOGIKA GENERATE & TAMPILAN ---
if generate_btn and ide_user:
    with st.spinner("Menganalisis ide dan merangkai adegan dengan Gemini..."):
        try:
            prompt = get_system_prompt(ide_user, niche, durasi, rasio, tone)
            
            # Memanggil API Gemini dan memaksa output berupa JSON
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            # Parsing JSON dari respon Gemini
            data = json.loads(response.text)
            
            # --- RENDER KE LAYAR STREAMLIT ---
            st.success("🎉 Script berhasil dibuat!")
            
            # Bagian Overview
            st.subheader("📌 Project Overview")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("**Alternatif Judul:**")
                for judul in data["project_overview"]["alternatif_judul"]:
                    st.write(f"- {judul}")
            with col2:
                st.write("**Prompt Thumbnail (Salin ke AI Image Generator):**")
                st.code(data["project_overview"]["thumbnail_image_prompt"], language="markdown")
            
            st.divider()
            
            # Bagian Hook
            st.subheader("🪝 Hook Pembuka")
            st.info(data["hook_pembuka"])
            
            st.divider()
            
            # Bagian Scene Builder (Looping Card)
            st.subheader("🎬 Scene Builder")
            for scene in data["scenes"]:
                with st.expander(f"Scene {scene['scene_number']} - {scene['estimated_duration']}", expanded=True):
                    st.write(f"**Visual:** {scene['visual_description']}")
                    st.code(scene['ai_image_prompt'], language="markdown")
                    st.markdown(f"> **Voice Over:** *\"{scene['narration_script']}\"*")
                    
        except json.JSONDecodeError:
            st.error("Gagal memproses data dari AI. Format JSON tidak valid.")
            st.write("Respon mentah:", response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan pada API Gemini: {e}")

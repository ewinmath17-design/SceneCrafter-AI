import streamlit as st
import json
# Import library AI pilihanmu (misal: openai, google.generativeai, dll)
# import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Cinemind Clone AI", page_icon="🎬", layout="wide")

st.title("🎬 AI Video Scene Builder")
st.markdown("Ubah satu ide menjadi naskah video panjang lengkap dengan prompt visual.")

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
    3. Visual Prompt: Tulis prompt gambar dalam bahasa Inggris yang detail.
    
    WAJIB OUTPUT DALAM FORMAT JSON BERIKUT TANPA TEKS LAIN:
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
    with st.spinner("Menganalisis ide dan merangkai adegan..."):
        try:
            prompt = get_system_prompt(ide_user, niche, durasi, rasio, tone)
            
            # TODO: Masukkan fungsi pemanggilan API AI di sini
            # Contoh dummy response (Hapus bagian ini dan ganti dengan respons AI asli)
            dummy_response = """
            {
              "project_overview": {
                "ide_utama": "Misteri Kapal Mary Celeste",
                "alternatif_judul": ["Misteri Terbesar Lautan", "Kru Menghilang Tanpa Jejak", "Mary Celeste: Fakta Tersembunyi"],
                "thumbnail_image_prompt": "Cinematic shot of an abandoned wooden ship floating on a misty ocean, dark and eerie atmosphere, 4k resolution, highly detailed."
              },
              "hook_pembuka": "Bayangkan kamu menemukan kapal utuh di tengah lautan, tapi tidak ada satu pun orang di dalamnya...",
              "scenes": [
                {
                  "scene_number": 1,
                  "estimated_duration": "15 detik",
                  "visual_description": "Kamera bergerak perlahan mendekati kapal berhantu di tengah kabut tebal.",
                  "ai_image_prompt": "Drone shot approaching an old 19th-century sailing ship, heavy fog, dark blue ocean, mysterious lighting, 16:9.",
                  "narration_script": "Pada 5 Desember 1872, kapal Mary Celeste ditemukan terombang-ambing di Samudra Atlantik."
                }
              ]
            }
            """
            
            # Parsing JSON (Pastikan API mengembalikan teks JSON bersih)
            data = json.loads(dummy_response) # Ganti dummy_response dengan hasil dari API
            
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
                st.write("**Prompt Thumbnail (Salin ke Midjourney):**")
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
            st.error("Gagal memproses data dari AI. Pastikan model AI mengembalikan format JSON yang valid.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

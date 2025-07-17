import streamlit as st
import yt_dlp
import os

# Page configuration
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Create downloads folder if it doesn't exist
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Downloader (403 Fixed)")

# Input from user
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose format:", ["🎥 Video", "🎵 Audio"])

if video_url and st.button("⬇️ Download Now"):
    try:
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

        ydl_opts = {
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": None,
            "format": (
                "bestaudio[ext=m4a]/bestaudio"
                if "Audio" in download_type
                else "best[ext=mp4]/best"
            ),
            "force_generic_extractor": False,
            "skip_download": False,
            "nocheckcertificate": True,
            "allow_unplayable_formats": False,
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/114.0.0.0 Mobile Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filepath = ydl.prepare_filename(info)

        if not os.path.exists(filepath):
            raise FileNotFoundError("Downloaded file not found!")

        with open(filepath, "rb") as f:
            st.success("✅ Download ready!")
            st.download_button(
                label="📥 Click to Save",
                data=f,
                file_name=os.path.basename(filepath),
                mime="audio/m4a" if "Audio" in download_type else "video/mp4"
            )

    except Exception as e:
        st.error(f"❌ Download failed: {e}")

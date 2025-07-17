import streamlit as st
import yt_dlp
import os

# Page config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Create downloads folder
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video and Audio Downloader")

# Inputs
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video", "🎵 Audio"])

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
            "http_headers": {
                # Mobile Safari UA
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/16.0 Mobile/15E148 Safari/604.1"
                )
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            downloaded_path = ydl.prepare_filename(info)

        if not os.path.exists(downloaded_path):
            raise FileNotFoundError("Downloaded file not found!")

        with open(downloaded_path, "rb") as f:
            st.success("✅ Download ready!")
            st.download_button(
                label="📥 Click to save",
                data=f,
                file_name=os.path.basename(downloaded_path),
                mime="audio/m4a" if "Audio" in download_type else "video/mp4"
            )

    except Exception as e:
        st.error(f"❌ Download failed: {e}")

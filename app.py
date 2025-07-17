import streamlit as st
import yt_dlp
import os

# Page setup
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Create downloads folder if not exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# App title
st.title("🎥 YouTube Video and Audio Downloader")

# User input
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video", "🎵 Audio"])

if video_url and st.button("⬇️ Download Now"):
    try:
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

        # yt-dlp options with manual User-Agent
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
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/114.0.0.0 Safari/537.36"
                )
            },
        }

        # Start download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            downloaded_path = ydl.prepare_filename(info)

        # Check if file exists
        if not os.path.exists(downloaded_path):
            raise FileNotFoundError("Downloaded file not found!")

        # Display download button
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

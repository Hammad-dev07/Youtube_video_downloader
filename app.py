import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video & Audio Downloader")

video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video (MP4)", "🎵 Audio (M4A)"])

if video_url and st.button("⬇️ Download Now"):
    try:
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

        ydl_opts = {
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": None,
            "format": "140" if "Audio" in download_type else "22/18/best[ext=mp4]/best",
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.youtube.com/"
            },
        }

        with st.spinner("Processing..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                downloaded_path = ydl.prepare_filename(info)

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

import streamlit as st
import yt_dlp
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")
st.title("🎥 YouTube Video Downloader")

video_url = st.text_input("📎 Paste YouTube video URL:")
filename = st.text_input("📝 Rename file (optional)")
choice = st.radio("Select download type:", ["Video (MP4)", "Audio (M4A)"])

if st.button("⬇️ Download"):
    if not video_url:
        st.error("⚠️ Please enter a valid YouTube URL.")
    else:
        try:
            output_template = os.path.join(
                DOWNLOAD_DIR, f"{filename}.%(ext)s") if filename else os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

            ydl_opts = {
                "outtmpl": output_template,
                "format": "bestaudio[ext=m4a]/bestaudio/best" if "Audio" in choice else "best[ext=mp4]/best",
                "quiet": True,
                "noplaylist": True,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                downloaded_file_path = ydl.prepare_filename(info)

            with open(downloaded_file_path, "rb") as file:
                st.success("✅ Download complete!")
                st.info("📁  File will be saved to your system when you click below:")
                st.download_button(
                    label="📥 Click to download",
                    data=file,
                    file_name=os.path.basename(downloaded_file_path),
                    mime="audio/mp4" if downloaded_file_path.endswith(".m4a") else "video/mp4"
                )

        except Exception as e:
            st.error(f"❌ Download failed: {e}")

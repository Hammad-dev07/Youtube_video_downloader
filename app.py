import streamlit as st
import yt_dlp
import os

# Page config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

st.title("🎥 YouTube Video & Audio Downloader")

# Input fields
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Select download type:", ["🎥 Video (MP4)", "🎵 Audio (M4A)"])

if video_url and st.button("⬇️ Download Now"):
    try:
        # Output path (no need to create folder)
        filename_template = "%(title)s.%(ext)s"

        # Use direct formats to avoid merge (so ffmpeg not required)
        ydl_opts = {
            "outtmpl": filename_template,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": None,  # no merging
            "format": (
                "bestaudio[ext=m4a]/bestaudio"
                if "Audio" in download_type
                else "best[ext=mp4]/best"
            ),
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/114.0.0.0 Safari/537.36"
            },
        }

        with st.spinner("Processing..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                downloaded_path = ydl.prepare_filename(info)

        if not os.path.exists(downloaded_path):
            raise FileNotFoundError("Downloaded file not found.")

        # Serve file to user
        with open(downloaded_path, "rb") as f:
            st.success("✅ Download ready!")
            st.download_button(
                label="📥 Click to save",
                data=f,
                file_name=os.path.basename(downloaded_path),
                mime="audio/m4a" if "Audio" in download_type else "video/mp4"
            )

        # Optionally delete file after download
        # os.remove(downloaded_path)

    except Exception as e:
        st.error(f"❌ Download failed: {e}")

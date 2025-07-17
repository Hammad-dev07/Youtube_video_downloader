import streamlit as st
import yt_dlp
import os

# Page config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Downloads folder (remove if you want everything in memory only)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video/Audio Downloader")

# Input
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video (MP4)", "🎵 Audio (M4A)"])

if video_url and st.button("⬇️ Download Now"):
    try:
        # Output file path
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

        # Format, MIME, merge logic
        if "Audio" in download_type:
            format_code = "bestaudio[ext=m4a]/bestaudio"
            merge_format = "m4a"
            mime_type = "audio/m4a"
        else:
            format_code = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            merge_format = "mp4"
            mime_type = "video/mp4"

        # yt_dlp config
        ydl_opts = {
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": merge_format,
            "format": format_code,
            "force_generic_extractor": False,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            downloaded_path = ydl.prepare_filename(info)

        with open(downloaded_path, "rb") as f:
            st.success("✅ Download ready!")
            st.download_button(
                label="📥 Click to save",
                data=f,
                file_name=os.path.basename(downloaded_path),
                mime=mime_type
            )

    except Exception as e:
        st.error(f"❌ Download failed: {e}")

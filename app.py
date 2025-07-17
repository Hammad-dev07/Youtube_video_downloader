import streamlit as st
import yt_dlp
import os

# Page configuration
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Set download folder (temp folder inside app)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Downloader (Mobile + Desktop Friendly)")

# User Input
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Download Type:", ["🎥 Video", "🎵 Audio"])

# Download Button
if video_url and st.button("⬇️ Download Now"):
    try:
        output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

        ydl_opts = {
            "outtmpl": output_path,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": None,
            "default_search": "auto",  # fallback to ytsearch if bad link
            "force_generic_extractor": True,  # helps avoid 403 in some mobile cases
            "format": (
                "bestaudio[ext=m4a]/bestaudio"
                if "Audio" in download_type
                else "best[ext=mp4]/bestvideo+bestaudio/best"
            ),
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/16.0 Mobile/15E148 Safari/604.1"
                )
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)

        if not os.path.exists(file_path):
            raise FileNotFoundError("Downloaded file not found.")

        with open(file_path, "rb") as f:
            st.success("✅ Download ready!")
            st.download_button(
                label="📥 Click to Save",
                data=f,
                file_name=os.path.basename(file_path),
                mime="audio/m4a" if "Audio" in download_type else "video/mp4"
            )

    except Exception as e:
        st.error(f"❌ Download failed: {e}")

import streamlit as st
import yt_dlp
import os

# Create a local downloads folder if it doesn't exist
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")
st.title("🎥YouTube video Downloader")

video_url = st.text_input("📎 Paste YouTube video URL:")
filename = st.text_input("📝 Rename file (optional)")
choice = st.radio("Select download type:", ["Video (best)", "Audio only (MP3)"])

if st.button("⬇️ Download"):
    if not video_url:
        st.error("⚠️ Please enter a valid YouTube URL.")
    else:
        try:
            output_template = os.path.join(DOWNLOAD_DIR, f"{filename}.%(ext)s") if filename else os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

            ydl_opts = {
                "outtmpl": output_template,
                "format": "bestaudio" if choice == "Audio only (MP3)" else "best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }] if choice == "Audio only (MP3)" else [],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                ext = 'mp3' if choice == "Audio only (MP3)" else info['ext']
                title = filename if filename else info['title']
                final_file_path = os.path.join(DOWNLOAD_DIR, f"{title}.{ext}")

            with open(final_file_path, "rb") as file:
                st.success("✅ Download complete!")
                st.info("📁 File saved in your browser's Downloads folder.")
                st.download_button(
                    label="📥 Click to download",
                    data=file,
                    file_name=f"{title}.{ext}",
                    mime="audio/mpeg" if ext == "mp3" else "video/mp4"
                )

        except Exception as e:
            st.error(f"❌ Download failed: {e}")

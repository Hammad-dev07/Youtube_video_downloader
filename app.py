import streamlit as st
import yt_dlp
import os

# Page config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Create downloads directory
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video/Audio Downloader")

video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video (MP4)", "🎵 Audio (M4A)"])

if video_url and st.button("⬇️ Download Now"):
    try:
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        progress = st.progress(0)
        status_text = st.empty()

        def progress_hook(d):
            if d["status"] == "downloading":
                percent = d.get("_percent_str", "0.0%").strip().replace("%", "")
                try:
                    progress.progress(min(int(float(percent)), 100))
                    status_text.text(f"⬇️ Downloading... {percent}%")
                except:
                    pass
            elif d["status"] == "finished":
                progress.progress(100)
                status_text.text("✅ Download complete!")
                progress.empty()
                status_text.empty()

        # Format selection without merge
        if "Audio" in download_type:
            format_code = "bestaudio[ext=m4a]/bestaudio"
            merge_format = None
        else:
            format_code = "best[ext=mp4]/best"
            merge_format = None  # Do not require merging

        ydl_opts = {
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": merge_format,
            "progress_hooks": [progress_hook],
            "format": format_code,
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
                mime="audio/m4a" if "Audio" in download_type else "video/mp4"
            )

    except Exception as e:
        st.error(f"❌ Download failed: {e}")

import streamlit as st
import yt_dlp
import os

# Page config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Create downloads directory if not exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video and Audio Downloader")

# User input
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video (MP4)", "🎵 Audio (M4A)"])

if video_url and st.button("⬇️ Download Now"):
    try:
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

        # Mobile-optimized yt_dlp settings
        ydl_opts = {
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": None,
            "format": (
                "bestaudio/best[height<=480]/best"
                if "Audio" in download_type
                else "best[height<=720][ext=mp4]/best[ext=mp4]/best"  # Mobile-friendly quality
            ),
            
            # Mobile browser headers
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/114.0.0.0 Mobile Safari/537.36"
            },
            
            # Mobile-specific extractors
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                    "player_skip": ["configs"]
                }
            },
            
            # Better error handling for mobile
            "ignoreerrors": False,
            "retries": 2,
            "fragment_retries": 2,
            "skip_unavailable_fragments": True,
        }

        with st.spinner("Processing..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                downloaded_path = ydl.prepare_filename(info)

        # Check if file exists
        if os.path.exists(downloaded_path):
            file_size = os.path.getsize(downloaded_path)
            st.success(f"✅ Download ready! ({file_size // (1024*1024)}MB)")
            
            # Mobile-friendly download
            with open(downloaded_path, "rb") as f:
                st.download_button(
                    label="📥 Click to save",
                    data=f,
                    file_name=os.path.basename(downloaded_path),
                    mime="audio/mp4" if "Audio" in download_type else "video/mp4"
                )
        else:
            st.error("❌ File not found after download")

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "403" in error_msg:
            st.error("❌ 403 Error - Mobile network issue")
            st.info("Try: Switch to WiFi, use different browser, or try audio download")
        elif "Requested format is not available" in error_msg:
            st.error("❌ Format not available")
            st.info("Try: Different video or switch to video download")
        elif "Sign in" in error_msg:
            st.error("❌ Video requires login")
        else:
            st.error(f"❌ Download failed: {error_msg}")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("💡 Try: Refresh page, check internet, or use different video")

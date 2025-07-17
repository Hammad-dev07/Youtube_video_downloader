import streamlit as st
import yt_dlp
import os
import time
import random

# Page config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video and Audio Downloader")

video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video", "🎵 Audio"])

if video_url and st.button("⬇️ Download Now"):
    try:
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

        # Enhanced ydl_opts with better error handling
        ydl_opts = {
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
            "merge_output_format": None,
            
            # User-Agent rotation to avoid detection
            "http_headers": {
                "User-Agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ])
            },
            
            # Retry settings
            "retries": 3,
            "fragment_retries": 3,
            "skip_unavailable_fragments": True,
            
            # Cookie handling
            "cookiefile": None,
            "cookiesfrombrowser": None,
            
            # Sleep between requests
            "sleep_interval": 1,
            "max_sleep_interval": 5,
            
            # Format selection with fallbacks
            "format": (
                "bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio"
                if "Audio" in download_type
                else "best[height<=720][ext=mp4]/best[ext=mp4]/best"
            ),
            
            # Additional options
            "extract_flat": False,
            "writethumbnail": False,
            "writeinfojson": False,
            
            # Geo-bypass options
            "geo_bypass": True,
            "geo_bypass_country": "US",
        }

        with st.spinner("🔄 Processing..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First extract info without downloading
                info = ydl.extract_info(video_url, download=False)
                st.info(f"📹 Title: {info.get('title', 'Unknown')}")
                st.info(f"⏱️ Duration: {info.get('duration', 'Unknown')} seconds")
                
                # Add small delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))
                
                # Now download
                info = ydl.extract_info(video_url, download=True)
                downloaded_path = ydl.prepare_filename(info)

        if os.path.exists(downloaded_path):
            with open(downloaded_path, "rb") as f:
                st.success("✅ Download ready!")
                st.download_button(
                    label="📥 Click to save",
                    data=f,
                    file_name=os.path.basename(downloaded_path),
                    mime="audio/m4a" if "Audio" in download_type else "video/mp4"
                )
        else:
            st.error("❌ File not found after download")

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "403" in error_msg:
            st.error("❌ 403 Forbidden Error - Try these solutions:")
            st.markdown("""
            **Possible fixes:**
            1. 🔄 Try again in a few minutes
            2. 🌐 Use a VPN (change your location)
            3. 📱 Try a different video URL
            4. 🔒 Check if video is private/restricted
            5. 🆕 Update yt-dlp: `pip install -U yt-dlp`
            """)
        elif "Video unavailable" in error_msg:
            st.error("❌ Video is unavailable or private")
        elif "Sign in" in error_msg:
            st.error("❌ Video requires sign-in to view")
        else:
            st.error(f"❌ Download error: {error_msg}")
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.info("💡 Try refreshing the page and trying again")

# Additional troubleshooting info
with st.expander("🔧 Troubleshooting Tips"):
    st.markdown("""
    **Common 403 Error Solutions:**
    
    1. **Update yt-dlp regularly:**
       ```bash
       pip install -U yt-dlp
       ```
    
    2. **Use different video quality:**
       - Try downloading lower quality videos
       - Some high-quality streams are more restricted
    
    3. **Check video accessibility:**
       - Make sure video is public
       - Try with different videos to test
    
    4. **Network issues:**
       - Try using VPN
       - Check your internet connection
       - Some regions have restrictions
    
    5. **Rate limiting:**
       - Wait a few minutes between downloads
       - Don't download too many videos quickly
    
    6. **Alternative formats:**
       - Try audio-only downloads
       - Use different format options
    """)

# Status info
st.sidebar.markdown("### 📊 Status")
st.sidebar.info("🟢 App is running")
st.sidebar.markdown("### 🔄 Updates")
st.sidebar.info("Keep yt-dlp updated for best results")
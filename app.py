import streamlit as st
import yt_dlp
import os
import time

# Page config
st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

# Create downloads directory if not exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video/Audio Downloader")

# User input
video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video (MP4)", "🎵 Audio (M4A)"])

if video_url and st.button("⬇️ Download Now"):
    success = False
    attempts = 0
    max_attempts = 5
    
    # Multiple configurations to try
    configs = [
        {
            "name": "Standard",
            "opts": {
                "format": "bestaudio/best[height<=480]/worst" if "Audio" in download_type else "best[height<=720]/worst",
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "web"]
                    }
                }
            }
        },
        {
            "name": "Mobile Android",
            "opts": {
                "format": "worst/best" if "Audio" in download_type else "worst[ext=mp4]/best[ext=mp4]",
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 Mobile Safari/537.36"
                },
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android"]
                    }
                }
            }
        },
        {
            "name": "iOS Safari",
            "opts": {
                "format": "worst/best",
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1"
                },
                "extractor_args": {
                    "youtube": {
                        "player_client": ["ios", "web"]
                    }
                }
            }
        },
        {
            "name": "YouTube TV",
            "opts": {
                "format": "worst",
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (SMART-TV; Linux; Tizen 2.4.0) AppleWebKit/538.1"
                },
                "extractor_args": {
                    "youtube": {
                        "player_client": ["tv", "web"]
                    }
                }
            }
        },
        {
            "name": "Basic (Last Resort)",
            "opts": {
                "format": "worst",
                "http_headers": {
                    "User-Agent": "yt-dlp/2023.07.06"
                }
            }
        }
    ]
    
    while not success and attempts < max_attempts:
        try:
            config = configs[attempts]
            
            with st.spinner(f"⏳ Method {attempts + 1}/{max_attempts}: {config['name']}..."):
                output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
                
                # Base options
                ydl_opts = {
                    "outtmpl": output_template,
                    "quiet": True,
                    "noplaylist": True,
                    "ignoreerrors": True,
                    "no_warnings": True,
                    "retries": 3,
                    "fragment_retries": 3,
                    "skip_unavailable_fragments": True,
                    "geo_bypass": True,
                    "writesubtitles": False,
                    "writeautomaticsub": False,
                    "writethumbnail": False,
                    "prefer_insecure": True,
                    "nocheckcertificate": True,
                }
                
                # Merge with config-specific options
                ydl_opts.update(config["opts"])
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    downloaded_path = ydl.prepare_filename(info)
                    
                    if os.path.exists(downloaded_path) and os.path.getsize(downloaded_path) > 0:
                        success = True
                        
                        file_size = os.path.getsize(downloaded_path)
                        st.success(f"✅ Downloaded with {config['name']} method! ({file_size // (1024*1024)}MB)")
                        
                        with open(downloaded_path, "rb") as f:
                            st.download_button(
                                label="📥 Click to save",
                                data=f,
                                file_name=os.path.basename(downloaded_path),
                                mime="audio/mp4" if "Audio" in download_type else "video/mp4"
                            )
                        break
                    else:
                        raise Exception("File not created or empty")
                
        except Exception as e:
            attempts += 1
            if attempts < max_attempts:
                st.warning(f"⚠️ Method {attempts} failed, trying next...")
                time.sleep(2)  # Longer delay before next attempt
            else:
                st.error(f"❌ All {max_attempts} methods failed!")
                st.info("🔧 Try: Update yt-dlp, use VPN, or try different video")
                
                # Show additional troubleshooting
                st.markdown("**Final troubleshooting:**")
                st.markdown("• Update: `pip install -U yt-dlp`")
                st.markdown("• Check if video is private/restricted")
                st.markdown("• Try with VPN (US/UK location)")
                st.markdown("• Use different network (WiFi/Mobile data)")
                st.markdown("• Try downloading from different device")
                st.markdown("• Some videos are permanently blocked")

# Status info
if st.sidebar.button("🔄 Update yt-dlp"):
    st.sidebar.code("pip install -U yt-dlp")
    st.sidebar.info("Run this in terminal")

st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown("• This tries 5 different methods")
st.sidebar.markdown("• Works with 99%+ videos")
st.sidebar.markdown("• Lower quality = higher success rate")
st.sidebar.markdown("• Some videos may be region-locked")
st.sidebar.markdown("• Update yt-dlp regularly for best results")
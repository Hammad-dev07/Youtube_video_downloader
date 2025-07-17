import streamlit as st
import yt_dlp
import os
import time

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("🎥 YouTube Video and Audio Downloader")

video_url = st.text_input("🔗 Paste YouTube URL:")
download_type = st.radio("Choose download type:", ["🎥 Video (MP4)", "🎵 Audio (M4A)"])

if video_url and st.button("⬇️ Download Now"):
    success = False
    attempts = 0
    max_attempts = 4
    
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
            st.info(f"🔄 Trying method {attempts + 1}: {config['name']}")
            
            output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
            
            ydl_opts = {
                "outtmpl": output_template,
                "quiet": True,
                "noplaylist": True,
                "ignoreerrors": True,
                "no_warnings": True,
                "retries": 2,
                "fragment_retries": 2,
                "skip_unavailable_fragments": True,
                "geo_bypass": True,
                "writesubtitles": False,
                "writeautomaticsub": False,
                "writethumbnail": False,
            }
            
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
                st.warning(f"⚠️ Method {attempts} failed: {str(e)[:50]}...")
                time.sleep(1)
                st.error(f"❌ All methods failed. Last error: {str(e)[:100]}...")
                st.info("🔧 Try: Update yt-dlp, use VPN, or try different video")

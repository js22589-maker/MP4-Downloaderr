import streamlit as st
import yt_dlp
import os

# --- UI Setup ---
st.set_page_config(page_title="MP4 Downloader", page_icon="🎬")
st.title("🎬 MP4 Video Downloader")
st.markdown("Paste a video link below to extract the MP4 file.")

# --- Functions ---
def download_video(url):
    try:
        # Save to the current directory
        save_path = os.getcwd()
        
        ydl_opts = {
            # Priority: Best MP4 available
            'format': 'best[ext=mp4]/best', 
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first to get the filename
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# --- Main Interface ---
url_input = st.text_input("Enter Video URL (YouTube, Vimeo, etc.):", placeholder="https://...")

if st.button("Process Video"):
    if url_input:
        with st.spinner("Downloading to server..."):
            file_path = download_video(url_input)
            
            if file_path and os.path.exists(file_path):
                st.success("Download Complete!")
                
                # Provide a button for the user to save the file from the server to their PC
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="Click to Save to your Device",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                # Optional: Clean up the file from the server after providing it
                # os.remove(file_path)
    else:
        st.warning("Please enter a valid URL.")

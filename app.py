import streamlit as st
import pandas as pd
import subprocess
import time
import sys
import webbrowser
import os

# ================= SPOTIFY PLAYLISTS =================
spotify_playlists = {
    "Happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "Sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "Angry": "https://open.spotify.com/playlist/37i9dQZF1DX1tyCD9QhIWF",
    "Fearful": "https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned",
    "Neutral": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
    "Surprised": "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
    "Disgusted": "https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4"
}

# ================= EMOTION COLORS & EMOJIS =================
emotion_style = {
    "Happy": ("#FFD93D", "😄"),
    "Sad": ("#4A6FA5", "😢"),
    "Angry": ("#FF4C4C", "😠"),
    "Fearful": ("#8E44AD", "😨"),
    "Neutral": ("#95A5A6", "😐"),
    "Surprised": ("#F39C12", "😲"),
    "Disgusted": ("#2ECC71", "🤢")
}

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Emotion Music System", layout="wide")

# ================= THEME TOGGLE =================
theme = st.toggle("🌗 Dark / Light Mode", value=True)

bg = "linear-gradient(135deg, #0f2027, #203a43, #2c5364)" if theme else "#f5f5f5"
text_color = "white" if theme else "#222"

st.markdown(f"""
<style>
.stApp {{
    background: {bg};
}}

.glass {{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 25px;
    margin: 20px auto;
    width: 70%;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    color: {text_color};
}}

.stButton>button {{
    background: linear-gradient(90deg, #1DB954, #1ed760);
    color: black;
    font-weight: bold;
    border-radius: 14px;
    padding: 0.8em 2em;
    border: none;
}}

h1, h2, h3 {{
    text-align: center;
    color: {text_color};
}}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1>🎵 Emotion Based Music Recommendation System</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>AI-powered facial emotion detection with Spotify playback</p>",
    unsafe_allow_html=True
)

# ================= LOAD DATA =================
df = pd.read_csv("muse_v3.csv")

df['link'] = df['lastfm_url']
df['name'] = df['track']
df['emotional'] = df['number_of_emotion_tags']
df['pleasant'] = df['valence_tags']
df = df[['name', 'emotional', 'pleasant', 'link', 'artist']]
df = df.sort_values(by=["emotional", "pleasant"]).reset_index(drop=True)

df_sad = df[:18000]
df_fear = df[18000:36000]
df_angry = df[36000:54000]
df_neutral = df[54000:72000]
df_happy = df[72000:]

def recommend_music(emotion):
    if emotion == "Happy":
        return df_happy.sample(8)
    elif emotion == "Angry":
        return df_angry.sample(8)
    elif emotion == "Fearful":
        return df_fear.sample(8)
    elif emotion == "Neutral":
        return df_neutral.sample(8)
    else:
        return df_sad.sample(8)

# ================= CENTER BUTTON =================
btn_col = st.columns([2,1,2])[1]
with btn_col:
    scan = st.button("📷 SCAN EMOTION")

# ================= MAIN FLOW =================
if scan:
    with st.spinner("🔍 Detecting emotion... Please look at the camera"):
        subprocess.run([sys.executable, "camera_emotion.py"])
        time.sleep(0.5)

    if not os.path.exists("emotion_result.txt"):
        st.error("Emotion detection failed. Please try again.")
    else:
        with open("emotion_result.txt", "r") as f:
            emotion, confidence = f.read().strip().split(",")

        color, emoji = emotion_style.get(emotion, ("#ffffff", "🙂"))

        # ================= RESULT CARD =================
        st.markdown(f"""
        <div class="glass" style="border-top:6px solid {color};">
            <h2>{emoji} Detected Emotion</h2>
            <p style="font-size:30px;"><b>{emotion}</b></p>
            <p>Confidence: {confidence}%</p>
        </div>
        """, unsafe_allow_html=True)

        # ================= SPOTIFY =================
        st.markdown(f"""
        <div class="glass">
            <h2>🎧 Music for Your Mood</h2>
            <a href="{spotify_playlists[emotion]}" target="_blank"
               style="color:#1DB954;font-size:22px;font-weight:bold;">
               ▶ Play on Spotify
            </a>
        </div>
        """, unsafe_allow_html=True)

        webbrowser.open(spotify_playlists[emotion])

        # ================= SONG GRID =================
        st.markdown("<h2>🎶 Recommended Songs</h2>", unsafe_allow_html=True)
        songs = recommend_music(emotion)
        cols = st.columns(4)

        for i, (_, row) in enumerate(songs.iterrows()):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="glass" style="width:100%;">
                    <b>{row['name']}</b><br>
                    <i>{row['artist']}</i><br>
                    <a href="{row['link']}" target="_blank">Open Link</a>
                </div>
                """, unsafe_allow_html=True)




# I refactored the original code to make it compatible with Streamlit. I removed desktop-specific OpenCV display calls and redundant logic, while preserving the core CNN-based emotion detection and recommendation pipeline.


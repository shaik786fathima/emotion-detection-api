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

# ================= READ EMOTION =================
if not os.path.exists("emotion_result.txt"):
    print("❌ emotion_result.txt not found. Run camera_emotion.py first.")
    exit()

with open("emotion_result.txt", "r") as f:
    emotion, confidence = f.read().strip().split(",")

print(f"Detected Emotion: {emotion} ({confidence}%)")

# ================= OPEN SPOTIFY =================
if emotion in spotify_playlists:
    print("🎵 Opening Spotify playlist...")
    webbrowser.open(spotify_playlists[emotion])
else:
    print("❌ No playlist found for this emotion")

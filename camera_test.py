import cv2
import time
import webbrowser

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




cap = cv2.VideoCapture(0)
time.sleep(1)

cv2.namedWindow("TEST CAMERA", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("TEST CAMERA", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




import cv2
import time
import webbrowser

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




cap = cv2.VideoCapture(0)
time.sleep(1)

cv2.namedWindow("TEST CAMERA", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("TEST CAMERA", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



# “The system maps each detected emotion to a predefined Spotify playlist and redirects playback to Spotify, avoiding direct media control.”
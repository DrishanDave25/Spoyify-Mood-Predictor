import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For resizing images

# Step 1: Spotify API authentication
CLIENT_ID = '77bff94e6824446a8d3190ccc39a8ad0'     
CLIENT_SECRET = '16bdee10aaac429d9e9ea3b6419202f5'  
# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                          client_secret=CLIENT_SECRET))

# Dataset
data = {
    'song': ['Song1', 'Song2', 'Song3', 'Song4', 'Song5', 'Song6', 'Song7', 'Song8'],
    'danceability': [0.8, 0.5, 0.9, 0.7, 0.6, 0.2, 0.95, 0.3],
    'energy': [0.9, 0.4, 0.7, 0.6, 0.8, 0.3, 0.9, 0.2],
    'valence': [0.95, 0.3, 0.8, 0.4, 0.9, 0.2, 0.6, 0.1],
    'tempo': [120, 130, 110, 115, 125, 70, 150, 60],
    'mood': ['happy', 'sad', 'working out', 'angry', 'happy', 'sleeping', 'working out', 'sleeping']
}

df = pd.DataFrame(data)

# Features and target variable
X = df[['danceability', 'energy', 'valence', 'tempo']]
y = df['mood']

# Step 3: Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Step 4: Predict the mood for a new song
def get_song_features(song_name, artist_name):
    result = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
    if not result['tracks']['items']:
        return None
    
    track_id = result['tracks']['items'][0]['id']
    features = sp.audio_features(track_id)[0]
    
    song_features = {
        'danceability': features['danceability'],
        'energy': features['energy'],
        'valence': features['valence'],
        'tempo': features['tempo']
    }
    return song_features

def predict_mood(song_name, artist_name):
    features = get_song_features(song_name, artist_name)
    if features is None:
        return "Song not found or features unavailable."
    
    feature_values = [[features['danceability'], features['energy'], features['valence'], features['tempo']]]
    mood_prediction = clf.predict(feature_values)[0]
    return mood_prediction

# Step 5: Create the Tkinter UI with resized logo
def on_predict():
    song_name = song_entry.get()
    artist_name = artist_entry.get()

    if not song_name or not artist_name:
        messagebox.showwarning("Input Error", "Please enter both song name and artist name.")
        return
    
    mood = predict_mood(song_name, artist_name)
    result_label.config(text=f"Predicted Mood: {mood}", fg="#007BFF")

# Initialize the main window
root = tk.Tk()
root.title("Spotify Mood Predictor")
root.geometry("500x450")
root.config(bg="#1DB954")  # Set background color to Spotify green

# Load and resize Spotify logo image
logo_image = Image.open("spotify_logo.png")  # Make sure you have 'spotify_logo.png'
logo_image = logo_image.resize((120, 120), Image.LANCZOS)  # Use LANCZOS for resizing
spotify_logo = ImageTk.PhotoImage(logo_image)

# Create a frame for better layout
main_frame = tk.Frame(root, bg="#1DB954")
main_frame.pack(pady=30)

# Display the Spotify logo
logo_label = tk.Label(main_frame, image=spotify_logo, bg="#1DB954")
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Title label
title_label = tk.Label(main_frame, text="Spotify Mood Predictor", font=("Helvetica", 20, "bold"), bg="#1DB954", fg="white")
title_label.grid(row=1, column=0, columnspan=2, pady=10)

# Song name label and entry
song_label = tk.Label(main_frame, text="Enter Song Name:", font=("Helvetica", 12), bg="#1DB954", fg="white")
song_label.grid(row=2, column=0, pady=10, padx=20, sticky="e")
song_entry = tk.Entry(main_frame, width=30, font=("Helvetica", 12))
song_entry.grid(row=2, column=1, pady=10)

# Artist name label and entry
artist_label = tk.Label(main_frame, text="Enter Artist Name:", font=("Helvetica", 12), bg="#1DB954", fg="white")
artist_label.grid(row=3, column=0, pady=10, padx=20, sticky="e")
artist_entry = tk.Entry(main_frame, width=30, font=("Helvetica", 12))
artist_entry.grid(row=3, column=1, pady=10)

# Predict Button
predict_button = tk.Button(main_frame, text="Predict Mood", command=on_predict, font=("Helvetica", 12), bg="#191414", fg="white", activebackground="#1DB954", activeforeground="white", relief="flat")
predict_button.grid(row=4, column=0, columnspan=2, pady=20)

# Label to display the result
result_label = tk.Label(main_frame, text="Predicted Mood: ", font=("Helvetica", 14, "bold"), bg="#191414", fg="white")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()

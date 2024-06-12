from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS module
import pymongo
import os
import random
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.pipeline import Pipeline

import subprocess

def convert_webm_to_wav(input_file, output_file):
    try:
        # Replace '/full/path/to/ffmpeg' with the actual path on your system
        ffmpeg_path = '/usr/local/bin/ffmpeg'
        
        # Run FFmpeg command with the full path
        subprocess.run([ffmpeg_path, '-i', input_file, output_file], check=True)
        print(f'Conversion completed: {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error during conversion: {e}')

# Replace 'input.webm' and 'output.wav' with your file names
input_webm_file = '/Users/nitin/Downloads/audio.webm'
# input_webm_file = 'audiosad.webm'


output_wav_file = 'output.wav'


# Function to process input songs and create a feature vector
def input_preprocessor(song_list, dataset):
    song_vectors = []
    
    # Extract features for each song in the input list
    for song in song_list:
        song_data = dataset[(dataset['Name'] == song['Name']) & (dataset['year'] == song['year'])]
        
        if not song_data.empty:
            # Append features to the song vector
            song_vectors.append(song_data.iloc[0][['valence', 'year', 'acousticness',
                                                   'danceability', 'energy', 'instrumentalness',
                                                   'liveness', 'loudness', 'speechiness', 'tempo']].values)
    
    # Calculate mean of song vectors if found, else return zeros
    if song_vectors:
        return np.mean(np.array(song_vectors), axis=0)
    else:
        return np.zeros(10)

def Music_Recommender(song_list, dataset, n_songs=10):
    features = ['valence', 'year', 'acousticness',
                'danceability', 'energy',
                'instrumentalness',
                'liveness', 'loudness',
                'speechiness', 'tempo']
    
    # Create a pipeline for clustering
    song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                      ('kmeans', KMeans(n_clusters=8))])
    X = dataset[features]
    song_cluster_pipeline.fit(X)
    
    # Process input songs to get their center
    song_center = input_preprocessor(song_list, dataset)
    scaler = song_cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(dataset[features])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    
    # Calculate distances between input song center and all songs
    ed_dist = euclidean_distances(scaled_song_center, scaled_data)
    index = list(np.argsort(ed_dist)[:,:n_songs][0])
    rec_output = dataset.iloc[index]
    
    # Filter out repeated song recommendations
    filtered_recommendations = []
    previous_song_name = None
    for _, song in rec_output.iterrows():
        song_name = song['Name']
        if song_name != previous_song_name:
            filtered_recommendations.append(song)
            previous_song_name = song_name
    rec_output = pd.DataFrame(filtered_recommendations)
    
    return rec_output[['year', 'Name', 'Artists', 'Album_x', 'Path','Emotion']]

# def query2(text):
#     print(text)

#     dataset = pd.read_csv('output_file_w_all.csv')

#     # Connect to MongoDB
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["Songs"]
#     music_collection = db["Combined"]

#     # Get user input for song name
#     requested_song_title = text
#     requested_song = music_collection.find_one({"Title": requested_song_title})
#     print(requested_song)

#     if requested_song:
#         # emotion = requested_song.get("Emotion", "Unknown Emotion")
#         requested_song_details = [{'Name': requested_song.get('Name'), 'year': requested_song.get('year')}]
#         recommendations = Music_Recommender(requested_song_details, dataset, n_songs=30)

#         songs = []
#         songs.append(requested_song)
#         if songs == None:
#             return 0
#         else:
#             # Collect recommended songs
#             for idx, song in recommendations.iterrows():
#                 songs.append(song)

#             # Set batch size and total number of songs
#             # batch_size = 15
#             # total_songs = len(songs)

#             # # Play songs in batches
#             # for batch_start in range(0, total_songs, batch_size):
#             #     batch_end = min(batch_start + batch_size, total_songs)
#             #     batch = songs[batch_start:batch_end]

#             #     # Print available songs in the batch
#             #     print(f"\nAvailable songs:")
#             #     for idx, song in enumerate(batch, start=batch_start + 1):
#             #         print(f"{idx}. {song['Name']}, {song['Artists']}, {song['Path']}")
#             #         #return(f"{idx}. {song['Name']}, {song['Artists']}, {song['Path']}")

#             #     break  
#     print(songs[:15])   
#     return (songs)
#     # Close MongoDB connection
#     # client.close()

def query2(text):
    # Initialize pygame mixer
    # pygame.mixer.init()
    print(text)

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Songs"]
    music_collection = db["Combined"]

    # Get user input for song name
    requested_song_title = text
    requested_song = music_collection.find_one({"Name": requested_song_title})
    print(requested_song)

    if requested_song:
        emotion = requested_song.get("Emotion", "Unknown Emotion")
        query2_result = list(music_collection.find({"Emotion": emotion, "Name": {"$ne": requested_song_title}}))

        # Create a list to store song information
        songs = []

        # Add the requested song at the beginning
        name = requested_song.get("Name", "Unknown Title")
        artist = requested_song.get("Artists", "Unknown Artist")
        # album = requested_song.get("Album", "Unknown Album")
        path = requested_song.get("Path", "")
        # songs.append({"Name": title, "Artists": artist, "album": album, "path": path})
        songs.append({"Name": name, "Artists": artist, "Path": path})


        # Retrieve other songs that match the emotion
        for song in query2_result:
            title = song.get("Name", "Unknown Title")
            artist = song.get("Artists", "Unknown Artist")
            # album = song.get("Album", "Unknown Album")
            path = song.get("Path", "")
            songs.append({"Name": title, "Artists": artist,  "Path": path})

        return songs[:15]
    else:
        return query1(text)



def query1(text):

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["Songs"]
    music_collection = db["Combined"]

    emotion = text
    print(emotion)
    query_result = music_collection.find({"Emotion": emotion})

    # Create a list to store song information
    songs = []

    for song in query_result:
        title = song.get("Name", "Unknown Title")  # Change to "Name" instead of "Title"
        artist = song.get("Artists", "Unknown Artist")
        path = song.get("Path", "")
        emotion = song.get("Emotion","")
        songs.append({"Name": title, "Artists": artist, "Path": path,"Emotion":emotion})

# Shuffle the songs list to get a random order
    random.shuffle(songs)

    print(songs[:15])   
    return (songs[:30])

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in your Flask app

@app.route('/api/data', methods=['GET'])
def get_data():
    songs = []
    input_webm_file = '/Users/nitin/Downloads/audio.webm'
    # input_webm_file = 'audiosad.webm'
    output_wav_file = 'output.wav'
    convert_webm_to_wav(input_webm_file, output_wav_file)
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        recordedaudio = recognizer.record(source)

    print('Printing the message..')
    text = recognizer.recognize_google(recordedaudio, language='en-US')
    print('Your message: {}'.format(text))

    # Sentiment analysis
    Sentence = [str(text)]
    analyser = SentimentIntensityAnalyzer()
    for i in Sentence:
        v = analyser.polarity_scores(i)

    # Custom formula for accurate mapping
    if v['compound'] >= 0.5:
        identified_emotion = "Happy"
    elif v['compound'] > -0.1 and v['compound'] < 0.5:
        identified_emotion = "Calm"
    elif v['compound'] > -0.5 and v['compound'] < -0.1:
        identified_emotion = "Sad"
    elif v['compound'] <= -0.1:
        identified_emotion = "Angry"

    try:
        if text.lower().startswith("play"):
            # Extract the song title from the recognized text
            words = text.split()  # Split the recognized text into words
            if len(words) >= 2 and words[0].lower() == "play":
                song_title = ' '.join(words[1:])  # Join the words after "play" to get the song title
                print('Song Title:', song_title)
                
                song_found = query2(song_title.lower())

                if song_found:
                    test3 = song_found
                    return jsonify(test3)
                    print(test3)
                else:
                    print("Song not found in the database.")
                    print("Detecting emotion...")
                    print("Emotion: ", identified_emotion)
                    test2 = query1(identified_emotion)
                    return jsonify(test2)


            else:
                print('No song title found in the message.')
                # If no song title found, treat it as a random phrase
                # test2 = query1(identified_emotion)
                # return {"test":test2}

        else:
            # print(identified_emotion)
            test1 = query1(identified_emotion)
            # return {"test":test1}
            return jsonify(test1)
    except Exception as ex:
        print('Error: Please say a phrase')

if __name__ == '__main__':
    app.run(debug=True,port = 5001)
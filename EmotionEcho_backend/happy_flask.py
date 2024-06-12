
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
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)

def happy_query():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["Songs"]
    music_collection = db["Combined"]

    emotion = "Happy"  # Setting the emotion to "Happy"
    print(emotion)
    query_result = music_collection.find({"Emotion": emotion})

    # Create a list to store song information
    songs = []

    # Retrieve songs that match the "Happy" emotion
    for song in query_result:
        title = song.get("Name", "Unknown Title")
        artist = song.get("Artists", "Unknown Artist")
        path = song.get("Path", "")
        emotion = song.get("Emotion","")
        songs.append({"Name": title, "Artists": artist, "Path": path,"Emotion":emotion})

    # Shuffle the songs list to get a random order
    random.shuffle(songs)

    # Return a subset of songs (first 15 or fewer)
    print(songs[:15])
    return songs[:15]

# Define a route for the happy_query function
@app.route('/api/happy_songs', methods=['GET'])
def get_happy_songs():
    songs = happy_query()
    return jsonify({"songs": songs})

if __name__ == '__main__':
    app.run(debug=True, port=2000)
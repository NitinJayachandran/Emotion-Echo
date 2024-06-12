import pymongo
import pygame
import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.pipeline import Pipeline

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

# Function to recommend music based on input songs
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
    
    return rec_output[['year', 'Name', 'Artists', 'Album_x', 'Path']]

# Function to handle user query and provide music recommendations
def query2(text):
    pygame.mixer.init()
    print(text)
    
    # Read dataset
    dataset = pd.read_csv('output_file_w_all.csv')
    
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Songs"]
    music_collection = db["Combined"]
    requested_song_title = text
    
    # Retrieve requested song details from MongoDB
    requested_song = music_collection.find_one({"Name": requested_song_title})
    print(requested_song)
    
    if requested_song:
        requested_song_details = [{'Name': requested_song.get('Name'), 'year': requested_song.get('year')}]
        recommendations = Music_Recommender(requested_song_details, dataset, n_songs=30)

        songs = []
        songs.append(requested_song)

        # Collect recommended songs
        for idx, song in recommendations.iterrows():
            songs.append(song)

        # Set batch size and total number of songs
        batch_size = 15
        total_songs = len(songs)

        # Play songs in batches
        for batch_start in range(0, total_songs, batch_size):
            batch_end = min(batch_start + batch_size, total_songs)
            batch = songs[batch_start:batch_end]

            # Print available songs in the batch
            print(f"\nAvailable songs:")
            for idx, song in enumerate(batch, start=batch_start + 1):
                print(f"{idx}. {song['Name']} - {song['Artists']}")
                print(f"\t ({song['Album_x']})")

            # Play songs in the batch
            for idx, song in enumerate(batch, start=batch_start + 1):
                print(f"\nPlaying {song['Name']} - {song['Artists']} ({idx}/{min(total_songs, batch_end)})")
                print(f"\t ({song['Album_x']})")
                pygame.mixer.music.load(song['Path'])
                pygame.mixer.music.play()

                while True:
                    choice = input("Press 'p' to pause, 'r' to resume, 'n' for next song, or 'b' for previous song: ").lower()
                    if choice == 'p':
                        pygame.mixer.music.pause()
                    elif choice == 'r':
                        pygame.mixer.music.unpause()
                    elif choice == 'n':
                        pygame.mixer.music.stop()
                        break
                    elif choice == 'b':
                        if idx > 0:
                            idx -= 2
                            song = songs[idx]
                            print(f"\nPlaying {song['Name']} - {song['Artists']} ({idx + 1}/{min(total_songs, batch_end)})")
                            print(f"\t ({song['Album_x']})")
                            pygame.mixer.music.load(song['Path'])
                            pygame.mixer.music.play()
                        else:
                            print("No previous song in the current batch.")
                    elif choice == 'q':
                        pygame.mixer.music.stop()
                        break

    # Close MongoDB connection
    client.close()

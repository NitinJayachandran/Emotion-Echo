import pymongo
import pygame
import os

def query1(text):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["Songs"]
    music_collection = db["Combined"]

    # Get user input for emotion
    emotion = text
    query_result = music_collection.find({"Emotion": emotion})

    # Create a set to store unique song paths
    unique_songs = set()

    # Create a list to store song information
    songs = []

    # Retrieve all unique songs that match the emotion
    for song in query_result:
        path = song.get("Path", "")
        if path not in unique_songs:
            unique_songs.add(path)
            title = song.get("Name", "Unknown Title")
            artist = song.get("Artists", "Unknown Artist")
            album = song.get("Album_x", "Unknown Album")
            songs.append({"title": title, "artist": artist, "album": album, "path": path})

    # Split the songs into sets of 15
    batch_size = 15
    for batch_start in range(0, len(songs), batch_size):
        batch_end = min(batch_start + batch_size, len(songs))
        batch = songs[batch_start:batch_end]

        # Display and play each set
        print("\nAvailable songs:")
        for idx, song in enumerate(batch, start=batch_start + 1):
            print(f"{idx}. {song['title']}")
            print(f"\t ({song['artist']}, {song['album']})")

        for idx, song in enumerate(batch, start=batch_start + 1):
            print(f"\nPlaying {song['title']} ({idx}/{batch_end})")
            print(f"\t ({song['artist']}, {song['album']})")
            pygame.mixer.music.load(song['path'])
            pygame.mixer.music.play()
            # input("Press Enter to stop playback...")
            # pygame.mixer.music.stop()
            
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
                        print(f"\nPlaying {song['title']} ({idx + 1}/{batch_end})")
                        print(f"\t ({song['artist']}, {song['album']})")
                        pygame.mixer.music.load(song['path'])
                        pygame.mixer.music.play()
                    else:
                        print("No previous song in the current batch.")
                elif choice == 'q':
                    pygame.mixer.music.stop()
                    break

    # Close the connection
    client.close()
# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# import os
# # from flask_cors import CORS 

# # app = Flask(__name__)
# # CORS(app)

# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, origins="*")

# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['Songs']  # Replace 'your_database_name' with your actual MongoDB database name
# collection = db['Combined']  # Replace 'your_collection_name' with your actual collection name

# def path_exists(path):
#     return os.path.exists(path)

# @app.route('/api/userfavorite', methods=['GET', 'POST'])
# def get_user_favorite():
#     try:
#         print("Connecting to MongoDB...")
#         # Check if the connection was successful by listing the collections in the database
#         collection_names = db.list_collection_names()

#         if collection_names:
#             print("Connected to MongoDB successfully")
#             print(f"Available collections: {', '.join(collection_names)}")
#         else:
#             print("No collections found in the database")

#         if request.is_json:
#             # Get data from the JSON request
#             data = request.get_json()
#         else:
#             # If not JSON, try getting form data
#             data = request.form.to_dict()

#         favoriteArtists = data.get('favoriteArtists', [])
#         print("Received favoriteArtists:", favoriteArtists)
#         projection = {"_id": 0, "Artists": 1, "Name": 1, "Path": 1}  # Include the "Path" field

#         # Query MongoDB to find songs by the favorite artists
#         songs = list(collection.find({"Artists": {"$in": favoriteArtists}}, projection))
#         print("Found songs:", songs)

#         # if songs:
#         #     # Adjust the response format to include "Path"
#         #     simplified_songs = [
#         #         {
#         #             "Artists": song.get("Artists", ""),
#         #             "Name": song.get("Name", ""),
#         #             "Path": song.get("Path", "")
#         #         }
#         #         for song in songs
#         #     ]
#         #     return jsonify({'songs': simplified_songs})
#         # else:
#         #     return jsonify({'songs': []})  # Return an empty list if no songs are found

#         unique_song_names = set()

#         # Filter out duplicates based on the song name
#         # unique_songs = [
#         #     {
#         #         "Artists": song.get("Artists", ""),
#         #         "Name": song.get("Name", ""),
#         #         "Path": song.get("Path", "")
#         #     }
#         #     for song in songs
#         #     if (song_name := song.get("Name", "")) not in unique_song_names and not unique_song_names.add(song_name)
#         # ]

#         # return jsonify({'favSongs': unique_songs})
#         unique_songs = []

#         for song in songs:
#             song_name = song.get("Name", "")
#             path = song.get("Path", "")

#             # Check if the file exists at the path
#             if song_name not in unique_song_names:
#                 unique_song_names.add(song_name)
#                 unique_songs.append({
#                     "Artists": song.get("Artists", ""),
#                     "Name": song_name,
#                     "Path": path
#                 })

#         # unique_songs = []

#         # for song in songs:
#         #     song_name = song.get("Name", "")
#         #     path = song.get("Path", "")

#         #     # Check if the file exists at the path
#         #     if path_exists(path):
#         #         # Add the song to the list
#         #         unique_songs.append({
#         #             "Artists": song.get("Artists", ""),
#         #             "Name": song_name,
#         #             "Path": path
#         #         })


#         return jsonify({'favSongs': unique_songs})


#     except Exception as e:
#         print(f"Failed to connect to MongoDB: {e}")
#         return str(e), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=8000)

from flask import Flask, request, jsonify
from pymongo import MongoClient
# from flask_cors import CORS 

# app = Flask(__name__)
# CORS(app)

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['Songs']  # Replace 'your_database_name' with your actual MongoDB database name
collection = db['Combined']  # Replace 'your_collection_name' with your actual collection name

@app.route('/api/userfavorite', methods=['GET', 'POST'])
def get_user_favorite():
    try:
        print("Connecting to MongoDB...")
        # Check if the connection was successful by listing the collections in the database
        collection_names = db.list_collection_names()

        if collection_names:
            print("Connected to MongoDB successfully")
            print(f"Available collections: {', '.join(collection_names)}")
        else:
            print("No collections found in the database")

        if request.is_json:
            # Get data from the JSON request
            data = request.get_json()
        else:
            # If not JSON, try getting form data
            data = request.form.to_dict()

        favoriteArtists = data.get('favoriteArtists', [])
        print("Received favoriteArtists:", favoriteArtists)
        projection = {"_id": 0, "Artists": 1, "Name": 1, "Path": 1}  # Include the "Path" field

        # Query MongoDB to find songs by the favorite artists
        songs = list(collection.find({"Artists": {"$in": favoriteArtists}}, projection))
        print("Found songs:", songs)

        # if songs:
        #     # Adjust the response format to include "Path"
        #     simplified_songs = [
        #         {
        #             "Artists": song.get("Artists", ""),
        #             "Name": song.get("Name", ""),
        #             "Path": song.get("Path", "")
        #         }
        #         for song in songs
        #     ]
        #     return jsonify({'songs': simplified_songs})
        # else:
        #     return jsonify({'songs': []})  # Return an empty list if no songs are found

        unique_song_names = set()

        # Filter out duplicates based on the song name
        unique_songs = [
            {
                "Artists": song.get("Artists", ""),
                "Name": song.get("Name", ""),
                "Path": song.get("Path", "")
            }
            for song in songs
            if (song_name := song.get("Name", "")) not in unique_song_names and not unique_song_names.add(song_name)
        ]

        return jsonify({'favSongs': unique_songs})


    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)

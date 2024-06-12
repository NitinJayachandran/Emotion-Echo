import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS module

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'output_file_w_all.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Replace 'your_column_name' with the actual name of the column you want to analyze
column_name = 'Artists'

# Get the count of unique elements in the specified column
unique_counts = df[column_name].value_counts()

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes by using the CORS() class

# Define a route to get the top 20 artists and their song counts
@app.route('/api/artists', methods=['GET'])
def get_top_artists():
    top_20_artists = unique_counts.head(20).reset_index()
    top_20_artists.columns = ['Artist', 'SongCount']
    result = top_20_artists.to_dict(orient='records')
    return jsonify(result)

# Run the Flask app on localhost:5000
if __name__ == '__main__':
    app.run(debug=True)

# import pandas as pd
# from pymongo import MongoClient

# # Replace 'your_file.csv' with the actual path to your CSV file
# file_path = 'output_file_w_all.csv'

# # Read the CSV file into a DataFrame
# df = pd.read_csv(file_path)

# # Replace 'your_column_name' with the actual name of the column you want to analyze
# column_name = 'Artists'

# # Get the count of unique elements in the specified column
# unique_counts = df[column_name].value_counts()

# # Get the top 20 artists
# top_20_artists = unique_counts.head(20).reset_index()
# top_20_artists.columns = ['Artist', 'SongCount']

# # Initialize MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
# db = client['ArtistList']  # Database name
# collection = db['Artists']  # Collection name

# # Convert DataFrame to a list of dictionaries
# artists_data = top_20_artists.to_dict(orient='records')

# # Insert data into MongoDB
# collection.insert_many(artists_data)

# print("Top 20 artists data has been inserted into the 'TopArtists' collection in the 'ArtistList' database.")



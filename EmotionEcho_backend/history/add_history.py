from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # Import the CORS module


app = Flask(__name__)
CORS(app)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['Users']  # Replace 'your_database_name' with your actual database name
history_collection = db['users']

@app.route('/api/addhistory', methods=['POST'])
def add_to_history():
    try:
        data = request.get_json()

        # Fetch user based on email
        email = data.get('email')
        user = history_collection.find_one({'email': email})

        if user:
            # Add the song to the listening history
            history_collection.update_one(
                {'_id': user['_id']},
                {'$push': {'listeningHistory': data['song']}}
            )

            return jsonify({'success': True, 'message': 'Song added to listening history'})
        else:
            return jsonify({'success': False, 'message': 'User not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True,port = 5655)

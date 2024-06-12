# # from flask import Flask, send_file, request
# # from pydub import AudioSegment
# # from pydub.playback import play
# # from urllib.parse import unquote
# # from flask_cors import CORS  # Import the CORS module

# # import os

# # app = Flask(__name__)
# # CORS(app)

# # AUDIO_FOLDER = ""

# # @app.route("/api/audio/<path:filename>",methods=['GET','POST'])
# # def serve_audio(filename):
# #     # decoded_filename = unquote(filename)
# #     # file_path = os.path.join(AUDIO_FOLDER, decoded_filename.replace("\\", "/"))
# #     # print("Current route path:", file_path)
    
# #     # # Load the audio file using pydub
# #     # audio = AudioSegment.from_file(file_path)
    
# #     # # Play the audio
# #     # play(audio)
    
# #     # # Return the audio file to the client
# #     # return send_file(file_path, mimetype="audio/mp3")

# #     try:
# #         data = request.json
# #         song_path = data.get("songPath")

# #         if not song_path:
# #             raise ValueError("Missing 'songPath' in the request body")

# #         decoded_path = unquote(song_path)
# #         file_path = os.path.join(AUDIO_FOLDER, decoded_path.replace("\\", "/"))
# #         print("Current route path:", file_path)

# #         audio = AudioSegment.from_file(file_path)

# #         # Play the audio
# #         play(audio)

# #         return send_file(file_path, mimetype="audio/mp3")

# #     except Exception as e:
# #         return str(e), 500


# # if __name__ == "__main__":
# #     app.run(host="0.0.0.0", port=5002, debug=True)


from flask import Flask, send_file,jsonify,request
from pydub import AudioSegment
from pydub.playback import play
from flask_cors import CORS
from urllib.parse import unquote

import os

app = Flask(__name__)
CORS(app)

AUDIO_FOLDER = ""

def clean_filename(filename):
    # Remove spaces from the filename
    return filename.replace(" ", "")

@app.route("/api/audio", methods=['GET','POST'])
def serve_audio():
    try:

        data = request.json
        song_path = data.get("songPath")

        if not song_path:
            raise ValueError("Missing 'songPath' in the request body")
        
        # Hardcoded address
        # original_filename = "5 Seconds of Summer - Easier.mp3"
        # cleaned_filename = clean_filename(original_filename)
        # file_path = f"/Users/nitin/Desktop/capstone/front_end_code/oldSongs/HappySongs/5 Seconds of Summer - Easier.mp3"

        decoded_path = unquote(song_path)
        file_path = os.path.join(AUDIO_FOLDER, decoded_path)
        print("Current route path:", file_path)


        print("Current route path:", file_path)
                
        # Load the audio file using pydub
        # audio = AudioSegment.from_file(file_path)

        # # Play the audio
        # play(audio)

        # Return the audio file to the client
        return send_file(file_path, mimetype="audio/mp3")
    
        response = jsonify({"status": "success", "message": "Song found and playing"})
        return response

    except Exception as e:
        # Return an error response if something goes wrong
        response = jsonify({"status": "error", "message": str(e)})
        return response, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)


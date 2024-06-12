from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
from up_Query2 import query2
from up_Query1 import query1

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print('Clearing background noise...')
    print('say any phrase or to request a song, sample phrase: play xyz ')
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print('Waiting for your message...')
    recordedaudio = recognizer.listen(source)
    print('Done recording..')

print('Printing the message..')
text = recognizer.recognize_google(recordedaudio, language='en-US')
print('Your message: {}'.format(text))

# Sentiment analysis
Sentence = [str(text)]
analyser = SentimentIntensityAnalyzer()
for i in Sentence:
    v = analyser.polarity_scores(i)

# Function to map the identified emotion to the playlistc
def map_emotion_to_playlist(emotion):
    mapping = {
        "Happy": "Energetic",
        "Sad": "Sad",
        "Angry": "Angry",
        "Calm": "Calm"
    }

    return mapping.get(emotion, "Unknown")  # Default set to "Unknown" if emotion not recognized

print(v)
# Custom formula for accurate mapping
if v['compound'] >= 0.5:
    identified_emotion = "Happy"
elif v['compound'] > -0.1 and v['compound'] < 0.5:
    identified_emotion = "Calm"
elif v['compound'] > -0.5 and v['compound'] < -0.1:
    identified_emotion = "Sad"
elif v['compound'] <= -0.55:
    identified_emotion = "Angry"

try:
    if text.lower().startswith("play"):
        # Extract the song title from the recognized text
        words = text.split()  # Split the recognized text into words
        if len(words) >= 2 and words[0].lower() == "play":
            song_title = ' '.join(words[1:])  # Join the words after "play" to get the song title
            print('Song Title:', song_title)
            song_found = query2(song_title.lower())

            if not song_found:
                print("Song not found in the database.")
                print("Detecting emotion...")
                print("Emotion: ", identified_emotion)
                query1(identified_emotion)
        else:
            print('No song title found in the message.')
            # If no song title found, treat it as a random phrase
            query1(identified_emotion)
    else:
        print(identified_emotion)
        query1(identified_emotion)
except Exception as ex:
    print('Error: Please say a phrase')
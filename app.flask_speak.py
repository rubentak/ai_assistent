# app.py

'''This is a basic Flask app that uses the terminal_chat_func.py file to run the chatbot functions. It also uses the gTTS library to convert the chatbot's answer to speech and the pygame library to play the audio. The speak_answer function is called in a new thread so that the chatbot can continue to run while the audio is playing.'''

from flask import Flask, render_template, request
from terminal_chat_func import run_all_functions
from gtts import gTTS
import pygame
import threading
import tempfile

# Initialize pygame mixer
pygame.mixer.init()

def speak_answer(answer):
    tts = gTTS(text=answer, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as f:
        tts.save(f.name)
        pygame.mixer.music.load(f.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transcript, answer = run_all_functions()
        # Call the speak_answer function in a new thread
        t = threading.Thread(target=speak_answer, args=(answer,))
        t.start()
        return render_template('index.html', transcript=transcript, answer=answer)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
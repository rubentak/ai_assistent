# app.py

'''This is a basic Flask app that uses the terminal_chat_func.py file to run the chatbot functions. It also uses the gTTS library to convert the chatbot's answer to speech and the pygame library to play the audio. The speak_answer function is called in a new thread so that the chatbot can continue to run while the audio is playing.'''

from flask import Flask, render_template, request
from terminal_chat_func import run_all_functions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transcript, answer = run_all_functions()
        return render_template('index.html', transcript=transcript, answer=answer)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

#%%

#%%

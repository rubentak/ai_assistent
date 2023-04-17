# app.py

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

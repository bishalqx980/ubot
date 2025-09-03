import os
from threading import Thread
from flask import Flask, render_template_string

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8080))

@app.route('/')
def index():
    return render_template_string("<h1>Working for now !! To be continued...!!!</h1>")

def run():
    app.run(host='0.0.0.0', port=PORT)

def alive():
    Thread(target=run).start()

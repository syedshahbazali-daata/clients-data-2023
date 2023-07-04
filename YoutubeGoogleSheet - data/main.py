from database import *
from updateLive import run_live_bot
from updateHome import run_bot
from updateContent import update_content
import threading
from flask import Flask

app = Flask(__name__)


@app.route("/alive")
def alive():
    return "Yes I am running"


def run_x():
    app.run(host='0.0.0.0', port=5000)


def keep_alive():
    threading.Thread(target=run_x).start()


def run():
    threading.Thread(target=run_live_bot).start()
    threading.Thread(target=run_bot).start()


keep_alive()
run()

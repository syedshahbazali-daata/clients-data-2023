import threading
from flask import Flask

app = Flask(__name__)


@app.route("/alive")
def alive():
    return "Yes I am running"


def run_x():
    app.run(host='0.0.0.0', port=6000)


def keep_alive():
    threading.Thread(target=run_x).start()


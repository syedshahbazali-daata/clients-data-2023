from database import *
from updateLive import run_live_bot
from updateContent import run_update_content
import threading
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route("/alive")
def alive():
  return "Yes I am running"


@app.route("/live-data", methods=["GET"])
def live_data():
  with open("live-data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
  print(data)
  return data


@app.route("/", methods=["GET", "POST"])
def home():
  if request.method == "POST":
    print("POST")
    input_type = request.form.get("type")
    input_url = request.form.get("url")
    if str(input_type).lower() == "playlist":
      with open("playlist.txt", 'w', encoding='utf-8') as file:
        file.write(input_url)

    else:
      with open("live_video_url.txt", 'w', encoding='utf-8') as file:
        file.write(input_url)

    return redirect(url_for("home"))

  live_extended_url = "https://www.youtube.com/watch?v=" + get_file_data(
    "live_video_url.txt")[0]
  return render_template("index.html",
                         live_video_url=live_extended_url,
                         playlist_url=get_file_data("playlist.txt")[0])


@app.route("/update-sheet", methods=["GET", "POST"])
def update_sheet():
  if request.method == "POST":
    print("POST")
    print(request.form)
    video_title = request.form.get("video-title")
    min_duration = int(request.form.get("min-duration"))
    total_duration = request.form.get("total-difference")
    get_content_data(video_title, min_duration, total_duration)

    return redirect(url_for("home"))
  video_list_data = get_videos_list()
  return render_template("filters-sheet.html", video_list_data=video_list_data)


def run_x():
  app.run(host='0.0.0.0', port=5000)



def run():
  threading.Thread(target=run_x).start()
  threading.Thread(target=run_live_bot).start()
  threading.Thread(target=run_update_content).start()


run()

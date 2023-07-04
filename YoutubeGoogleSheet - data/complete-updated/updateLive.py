from datetime import datetime

from database import *
from youtubesearchpython import VideosSearch  # pip install youtube-search-python==1.6.2
import json
import youtubesearchpython



def get_views(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    videos_search = VideosSearch(url, limit=1)
    result = videos_search.result()
    try:
        vide_tittle = str(result['result'][0]['title']).strip()
        views_count = int(str(result['result'][0]['viewCount']['text']).strip().replace(",", "").split(" ")[0])

        return [vide_tittle, views_count]

    except:
        return None


def run_live_bot():
    while True:
        live_video_url = get_file_data("live_video_url.txt")
        if len(live_video_url) > 0 and live_video_url[0] != '':
            data = get_views(live_video_url[0])
            if data is not None:
                video_title = data[0]
                views_count = data[1]

                # save into json file
                with open("live-data.json", 'w', encoding='utf-8') as file:
                    json.dump({"title": video_title, "views": views_count}, file, indent=4)


            print("Updated Live Data")

        time.sleep(10)

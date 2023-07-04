from datetime import datetime

from database import *
from youtubesearchpython import VideosSearch  # pip install youtube-search-python==1.6.2

import youtubesearchpython



def get_views(video_id):
    videos_search = VideosSearch(video_id, limit=1)
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
            record = []
            record.extend(data)
            date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            record.append(date_time)
            update_row(record, 'LIVE')
            print("Updated Live Data")

        time.sleep(2 * 60)

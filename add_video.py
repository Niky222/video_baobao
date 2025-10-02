import feedparser
from sql import init_db, save_video_id


def get_latest_shorts():
    max_results = 100
    channel_ids = ["UCDk2GktohtUW8ISE8pScIIg", "UC5sR6QxQ_IGuYLdKiAuRC9g", "UCIQkB66MZHCXmCd_fMTYF4g", "UCWv9OQrW_RSiiRq9QXjJoyA", "UCp2WMxeYQdVCiecCk4AiRQQ", "UCbTTzMc6ChtpgNQtLtdopSg","UCW737FlIIxBBKGgza1YcMJA"]
    shorts_ids = []

    for channel_id in channel_ids:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        feed = feedparser.parse(url)

        if not feed.entries:
            print(f"⚠️ Не удалось получить видео с канала {channel_id}")
            continue

        # фильтруем только shorts
        for entry in feed.entries[:max_results]:
            if "shorts/" in entry.link:  # проверка на формат Shorts
                shorts_ids.append(entry.yt_videoid)

    init_db()  # создаём базу, если её ещё нет
    for vid in shorts_ids:
        save_video_id(vid)

if __name__ == "__main__":
    get_latest_shorts()

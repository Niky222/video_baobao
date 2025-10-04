import feedparser
from sql import init_db, save_video_id


def get_latest_shorts():
    max_results = 100
    channel_ids = [
        "UCDk2GktohtUW8ISE8pScIIg",
        "UC5sR6QxQ_IGuYLdKiAuRC9g",
        "UCIQkB66MZHCXmCd_fMTYF4g",
        "UCWv9OQrW_RSiiRq9QXjJoyA",
        "UCp2WMxeYQdVCiecCk4AiRQQ",
        "UCbTTzMc6ChtpgNQtLtdopSg",
        "UCW737FlIIxBBKGgza1YcMJA"
    ]

    shorts = []  # ✅ Исправлено: теперь переменная существует

    for channel_id in channel_ids:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        feed = feedparser.parse(url)

        if not feed.entries:
            print(f"⚠️ Не удалось получить видео с канала {channel_id}")
            continue

        for entry in feed.entries[:max_results]:
            if "shorts/" in entry.link.lower():  # фильтр на Shorts
                shorts.append((entry.yt_videoid, entry.title))

    # Создание базы, если её ещё нет
    init_db()

    # Сохранение результатов
    for vid, title in shorts:
        save_video_id(vid, title)

    print(f"✅ Добавлено {len(shorts)} видео.")


if __name__ == "__main__":
    get_latest_shorts()

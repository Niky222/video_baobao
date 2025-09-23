import requests
import subprocess
import json
import feedparser
from sql import init_db, save_video_id, get_all_video_ids, update_video_status


def download_youtube_video(video_id, output_file):
    api_url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_short/{video_id}"
    headers = {
        "x-rapidapi-host": "youtube-video-fast-downloader-24-7.p.rapidapi.com",
        "x-rapidapi-key": "67986ba9cemshbb17d65db207fc3p110386jsne22a822448d8"
    }

    params = {
        "quality": 247
    }

    print(f"📥 Скачиваем видео ID: {video_id} ...")
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ Ошибка API: {response.status_code}, {response.text}")
        update_video_status(video_id, "failed", "videos.db")
        return False

    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))

    video_url = data.get("file")
    if not video_url:
        print(f"❌ Ссылка на видео не найдена в JSON.")
        update_video_status(video_id, "failed", "videos.db")
        return False

    video_resp = requests.get(video_url, stream=True)
    if video_resp.status_code == 200:
        with open(output_file, "wb") as f:
            for chunk in video_resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"✅ Видео {video_id} сохранено как {output_file}")
        update_video_status(video_id, "downloaded", "videos.db")
        return True
    else:
        print(f"❌ Ошибка при скачивании видео: {video_resp.status_code}")
        update_video_status(video_id, "failed", "videos.db")
        return False



# --- Функция наложения видео через FFmpeg ---
def overlay_videos_ffmpeg(main_video, square_video, output_video):
    # Получаем размеры основного видео
    cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "{main_video}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    width, height = map(int, result.stdout.strip().split(','))

    # Размер квадратного видео (1/3 от ширины основного)
    square_size = int(width / 1.5)

    # Позиция квадратного видео (по центру внизу)
    x_pos = 0
    y_pos = height - square_size + 50

    cmd = [
        'ffmpeg',
        '-i', main_video,
        '-i', square_video,
        '-filter_complex',
        f'[1:v]scale={square_size}:{square_size}[small];[0:v][small]overlay={x_pos}:{y_pos}',
        '-c:a', 'copy',
        '-y',
        output_video
    ]

    subprocess.run(cmd, check=True)
    print(f"Результат наложения видео сохранен в {output_video}")



API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5pa2l0YWQ1ODkwQGdtYWlsLmNvbSIsImV4cCI6NDkxMTc4ODU2MywianRpIjoiOTc2MjM1ZjctZDEwMy00NDgxLWI2NzItODQ4OWFkODgyYzlhIn0.FgyGGk3ymOnA_4GwKTwVFvA2dc0h2NFm0TCcxbE9ntw"

def upload(social, video_path, title):
    url = "https://api.upload-post.com/api/upload"
    headers = {
        "Authorization": f"Apikey {API_KEY}"
    }
    data = {
        "title": title,
        "user": "baobao",
        "platform[]": {social}  # 👈 ключевое — загружаем на Instagram
    }
    files = {
        "video": open(video_path, "rb")
    }

    response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code == 200:
        print("✅ Видео успешно отправлено")
        print(response.json())
        return response.json()
    else:
        print(f"❌ Ошибка загрузки ({response.status_code}): {response.text}")
        return None

if __name__ == "__main__":
    new_videos = [v for v in get_all_video_ids() if v["status"] == "new"]

    main_video_id = new_videos[0]['video_id']
    download_youtube_video(main_video_id, "main.mp4")
    print(get_all_video_ids())
    overlay_videos_ffmpeg("main.mp4", "bao.mp4", "res.mp4")
    upload(social ="tiktok", video_path="res.mp4", title="Изучайте китайский на https://baobao.by")
    upload(social="youtube", video_path="res.mp4", title="Изучайте китайский на https://baobao.by")
    upload(social="instagram", video_path="res.mp4", title="Изучайте китайский на https://baobao.by")




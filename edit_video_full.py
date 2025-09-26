import subprocess

def concat_videos_ffmpeg(video1, video2, output_video):
    # Временные перекодированные файлы
    tmp1 = "tmp1.mp4"
    tmp2 = "tmp2.mp4"

    # Шаг 1: перекодируем первое видео (обрезаем до 10 секунд)
    subprocess.run([
        "ffmpeg", "-i", video1,
        "-t", "10",  # обрезка по длительности
        "-vf", "scale=1080:1920,setsar=1",
        "-c:v", "libx264", "-crf", "23", "-preset", "fast",
        "-c:a", "aac", "-ar", "44100", "-ac", "2",
        "-y", tmp1
    ], check=True)

    # Шаг 2: перекодируем второе видео без обрезки
    subprocess.run([
        "ffmpeg", "-i", video2,
        "-vf", "scale=1080:1920,setsar=1",
        "-c:v", "libx264", "-crf", "23", "-preset", "fast",
        "-c:a", "aac", "-ar", "44100", "-ac", "2",
        "-y", tmp2
    ], check=True)

    # Шаг 3: создаём текстовый файл со списком для конкатенации
    with open("list.txt", "w") as f:
        f.write(f"file '{tmp1}'\n")
        f.write(f"file '{tmp2}'\n")

    # Шаг 4: конкатенация без повторного перекодирования
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "list.txt", "-c", "copy", "-y", output_video
    ], check=True)

    print(f"Склеенные видео сохранены в {output_video}")

if __name__ == "__main__":
    concat_videos_ffmpeg("main.mp4", "full.mp4", "res.mp4")

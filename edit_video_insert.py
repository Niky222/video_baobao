import subprocess

def get_video_duration(video_path: str) -> float:
    """Возвращает длительность видео в секундах (float)."""

    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f"⚠️ Не удалось получить длительность видео: {result.stderr}")

    try:
        return float(result.stdout.strip())
    except ValueError:
        raise ValueError(f"⚠️ Некорректное значение длительности: {result.stdout.strip()}")

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
    
def overlay_videos_ffmpeg(main_video, insert_video, output_video):
    # --- Получаем размеры основного видео ---
    cmd_main = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "{main_video}"'
    result_main = subprocess.run(cmd_main, shell=True, capture_output=True, text=True)
    width_main, height_main = map(int, result_main.stdout.strip().split(','))

    # --- Получаем размеры вставляемого видео ---
    cmd_insert = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "{insert_video}"'
    result_insert = subprocess.run(cmd_insert, shell=True, capture_output=True, text=True)
    width_insert, height_insert = map(int, result_insert.stdout.strip().split(','))

    # --- Масштабируем вставляемое видео ---
    # хотим, чтобы оно занимало примерно 1/3 ширины основного видео, сохраняя пропорции
    target_width = int(width_main / 3)
    aspect_ratio = height_insert / width_insert
    target_height = int(target_width * aspect_ratio)

    # --- Вычисляем позицию вставки ---
    x_pos = (width_main - target_width) // 2  # по центру по горизонтали
    y_pos = height_main - target_height - 10  # снизу с отступом 50px

    cmd = [
        'ffmpeg',
        '-i', main_video,
        '-i', insert_video,
        '-filter_complex',
        f'[1:v]scale={target_width}:{target_height}[small];[0:v][small]overlay={x_pos}:{y_pos}',
        '-c:a', 'copy',
        '-y',
        output_video
    ]

    subprocess.run(cmd, check=True)
    print(f"Результат наложения видео сохранен в {output_video}")


if __name__ == "__main__":
    if get_video_duration(video_path: str) < 15:
        concat_videos_ffmpeg("main.mp4", "insert.mp4", "res.mp4")
    else:     
        overlay_videos_ffmpeg("main.mp4", "insert.mp4", "res.mp4")

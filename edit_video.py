import os
import subprocess

def overlay_videos_ffmpeg(main_video, square_video, output_video):
    main_path = os.path.join(os.getcwd(), main_video)
    square_path = os.path.join(os.getcwd(), square_video)
    output_path = os.path.join(os.getcwd(), output_video)

    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        main_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("ffprobe stdout:", repr(result.stdout))
    print("ffprobe stderr:", repr(result.stderr))

    if not result.stdout.strip():
        raise ValueError(f"Не удалось получить размеры видео {main_video}")

    width, height = map(int, result.stdout.strip().split(','))
    print(f"Размеры видео: {width}x{height}")

    # Пример команды overlay, если нужно
    ffmpeg_cmd = [
        'ffmpeg', '-i', main_path, '-i', square_path,
        '-filter_complex', f'overlay=10:10',
        '-y', output_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Видео сохранено как {output_video}")


if __name__ == "__main__":
    overlay_videos_ffmpeg("main.mp4", "bao.mp4", "res.mp4")

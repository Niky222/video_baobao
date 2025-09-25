import subprocess

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
    overlay_videos_ffmpeg("main.mp4", "insert.mp4", "res.mp4")

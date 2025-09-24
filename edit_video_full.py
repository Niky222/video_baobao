import subprocess

def concat_videos_ffmpeg(video1, video2, output_video):
    cmd = [
        "ffmpeg",
        "-i", video1,
        "-i", video2,
        "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]",
        "-map", "[a]",
        "-y",
        output_video
    ]
    subprocess.run(cmd, check=True)
    print(f"Склеенные видео сохранены в {output_video}")

if __name__ == "__main__":
    concat_videos_ffmpeg("main.mp4", "full.mp4","res.mp4")

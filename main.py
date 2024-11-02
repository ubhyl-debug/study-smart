# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from openai import OpenAI
from moviepy.editor import VideoFileClip
import subprocess
import os

def split_video(video_path, segment_length="00:10:00", output_format="output%03d.mp4"):
    """
    Splits the video into segments using ffmpeg without re-encoding.
    """
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-c', 'copy',
        '-map', '0',
        '-segment_time', segment_length,
        '-f', 'segment',
        output_format
    ]
    subprocess.run(cmd, check=True)

def transcribe_audio(audio_path, client):
    """
    Transcribes the audio file using the OpenAI API.
    """
    with open(audio_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

if __name__ == '__main__':
    api_key = os.getenv('OPENAI_API_KEY')
    video_path = os.getenv('VIDEO_PATH')

    if not api_key or not video_path:
        raise ValueError("Environment variables OPENAI_API_KEY or VIDEO_PATH not set")

    client = OpenAI(api_key=api_key)
    split_video(video_path)  # Split the video into segments

    for segment in sorted(os.listdir('.')):
        if segment.startswith('output') and segment.endswith('.mp4'):
            video_clip = VideoFileClip(segment)
            audio_path = segment.replace('.mp4', '.mp3')
            video_clip.audio.write_audiofile(audio_path)
            transcript_text = transcribe_audio(audio_path, client)

            # Save the transcript to a text file
            with open(f'transcript_{segment}.txt', 'w') as file:
                file.write(transcript_text)
            print(f"The transcript has been saved to 'transcript_{segment}.txt'.")

    print("All segments have been processed.")

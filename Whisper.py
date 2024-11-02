import base64
import os
import subprocess
import string
from dataclasses import dataclass, field
from moviepy.editor import VideoFileClip
from typing import Dict, List, Optional, Tuple
from functools import cached_property, lru_cache
from openai import OpenAI

# Import and setup other necessary parts from code2

@dataclass
class VideoProcessor:
    video_path: str
    segment_length: str = "00:10:00"
    output_format: str = "output%03d.mp4"
    api_key: str = None
    client: OpenAI = field(init=False)

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("API key is required for transcription.")
        self.client = OpenAI(api_key=self.api_key)

    def split_video(self):
        """
        Splits the video into segments using ffmpeg without re-encoding.
        """
        cmd = [
            'ffmpeg',
            '-i', self.video_path,
            '-c', 'copy',
            '-map', '0',
            '-segment_time', self.segment_length,
            '-f', 'segment',
            self.output_format
        ]
        subprocess.run(cmd, check=True)

    def transcribe_audio(self, audio_path):
        """
        Transcribes the audio file using the OpenAI API.
        """
        with open(audio_path, 'rb') as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text

    def process_video(self):
        self.split_video()
        for segment in sorted(os.listdir('.')):
            if segment.startswith('output') and segment.endswith('.mp4'):
                video_clip = VideoFileClip(segment)
                audio_path = segment.replace('.mp4', '.mp3')
                video_clip.audio.write_audiofile(audio_path)
                transcript_text = self.transcribe_audio(audio_path)
                # Save the transcript to a text file
                with open(f'transcript_{segment}.txt', 'w') as file:
                    file.write(transcript_text)
                print(f"The transcript has been saved to 'transcript_{segment}.txt'.")

# Utilize other parts of code2 here

if __name__ == '__main__':
    video_processor = VideoProcessor(
        video_path=os.getenv('VIDEO_PATH'),
        api_key=os.getenv('OPENAI_API_KEY')
    )
    video_processor.process_video()

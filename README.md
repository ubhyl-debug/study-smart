# Study Smart Lecture Transcription Tool

This repository contains two Python scripts designed to help students transcribe their lectures effortlessly. Whether you're attending live lectures or reviewing recorded sessions, these scripts will save you time by converting audio into text.

## Features
- **Transcription Service**: Transcribes video files into text format using a speech-to-text API (e.g., OpenAI's Whisper or similar).

## Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/) (for installing required packages)
- [OpenAI API Key](https://platform.openai.com/signup)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ubhyl-debug/study-smart.git
   cd study-smart

2. Install requirements:
   ```bash
   pip install -r requirements.txt

3. You can set these variables in your shell session:
   ```bash
   export OPENAI_API_KEY='your_openai_api_key'
   export VIDEO_PATH='/path/to/your/lecture_audio_or_video.mp4'

Alternatively, you can add them to your .bashrc or .zshrc file for persistent use.

4. Run main file to get transcript:
   ```bash
   python main.py
   

   
   

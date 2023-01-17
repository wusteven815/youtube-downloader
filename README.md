<div align="center">

  # YouTube to MP3/MP4

  A simple command line based YouTube to MP3/MP4 downloader.
  
  ![](https://img.shields.io/github/license/wusteven815/youtube-downloader)
  ![](https://img.shields.io/github/v/release/wusteven815/youtube-downloader)
  ![](https://img.shields.io/github/last-commit/wusteven815/youtube-downloader)

</div>

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Installation/Usage](#installationusage)
  - [Windows](#windows)
  - [Linux](#linux)

# Features

- Input your own custom title, album, artist, and cover metadata to mp3s
- Choose between 720p and 1080p mp4 quality
  - Automatically determines the best 1080p format if chosen

# Installation/Usage

The project uses Python3. The [eyed3 library](https://github.com/nicfit/eyeD3) is used to mp3 metadata. The project also uses the [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [ffmpeg](https://github.com/FFmpeg/FFmpeg) binaries. They come included with the repository but if you want to download you're own, make sure the file name remains unchanged.

The program runs the installer in an infinite loop. To exit, either close the window or press `Ctrl+C`.

## Windows

1. Clone the repository

```bash
git clone https://github.com/wusteven815/youtube-downloader.git
cd youtube-downloader
```

2. (Optional) Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate.bat
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Run the program

```bash
python main.py
```

## Linux

1. Clone the repository

```bash
git clone https://github.com/wusteven815/youtube-downloader.git
cd youtube-downloader
```

2. (Optional) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies

```bash
pip3 install -r requirements.txt
```

4. Run the program

```bash
python3 main.py
```

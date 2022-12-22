from os import remove
from os import replace
from subprocess import PIPE
from subprocess import Popen
from subprocess import run
from sys import stdout
from tkinter import Tk
from tkinter import filedialog

from eyed3 import load as eyed3_load


def live_stdout_run(*cmd):

    process = Popen(cmd, stdout=PIPE, shell=True)
    for c in iter(lambda: process.stdout.read(1), b""):
        stdout.buffer.write(c)
    process.wait()

    return process


class Downloader:

    def __init__(self):

        self.tk = Tk()
        self.tk.attributes("-topmost", True)
        self.tk.withdraw()

        self.url = ""
        self.file_type = ""
        self.temp_file = ""

    def main(self):

        self.url = input(">>> YouTube Video URL: ")
        self.file_type = input(">>> File Type (mp3/mp4): ")
        self.temp_file = f"ytdl-temp.{self.file_type}"

        match self.file_type:
            case "mp3":
                self.download_mp3()
            case "mp4":
                self.download_mp4()
            case _:
                print("(!) Invalid file type")

    def save_file(self, initial_name):

        fp = filedialog.asksaveasfilename(filetypes=[(self.file_type.upper(), f"*.{self.file_type}")],
                                          initialfile=initial_name)

        if fp == "":
            remove(self.temp_file)
            print("(!) Cancelled")
        elif fp.endswith(f".{self.file_type}"):
            replace(self.temp_file, fp)
            print("(*) Completed")
        else:
            replace(self.temp_file, f"{fp}.{self.file_type}")
            print("(*) Completed")

    def download_mp3(self):

        console_res = live_stdout_run("ytdlp", self.url, "-o", self.temp_file, "-x", "--audio-format", "mp3")

        if console_res.returncode != 0:
            return

        name = input(">>> Music Title: ")
        album = input(">>> Music Album: ")
        artist = input(">>> Music Artist: ")

        print(">>> Cover Image: ", end="")
        cover = filedialog.askopenfilename(filetypes=[("PNG", ".png"), ("JPG", ".jpg"), ("JPEG", ".jpeg")],
                                           title="Open cover image")
        if cover == "":
            print("None selected")
        else:
            print(cover)

        metadata = eyed3_load(self.temp_file)
        metadata.initTag(version=(2, 3, 0))
        metadata.tag.title = name
        metadata.tag.album = album
        metadata.tag.artist = artist

        if cover != "":
            with open(cover, "rb") as cover_file:
                metadata.tag.images.set(3, cover_file.read(), "image/jpeg", u"Cover")

        metadata.tag.save()

        self.save_file(name)

    def download_mp4(self):

        quality = input(">>> Video Quality (720/1080): ")
        match quality:
            case "720":
                self.download_mp4_720()
            case "1080":
                self.download_mp4_1080()
            case _:
                print("(!) Invalid quality")

    def download_mp4_720(self):

        res = live_stdout_run("ytdlp", self.url, "-o", f"ytdl-temp.{self.file_type}", "-f", "mp4")
        if res.returncode != 0:
            return

        self.save_file("download")

    def download_mp4_1080(self):

        res = run(("ytdlp", "-F", self.url), capture_output=True, shell=True)
        if res.returncode != 0:
            print("(!) " + res.stderr.decode("utf-8")[7:-1])
            return

        m4a_format = "-1"
        hd_mp4_format = "-1"
        for line in (line[:32].split() for line in res.stdout.decode("utf-8").split("\n")):
            if len(line) > 2:
                if line[1] == "m4a" and line[2] == "audio":
                    m4a_format = line[0]
                elif line[1] == "mp4" and line[2] == "1920x1080":
                    hd_mp4_format = line[0]

        if m4a_format == "-1":
            print("(!) No m4a found. Try downloading manually.")
            return
        if hd_mp4_format == "-1":
            print("(!) No 1920x1080 mp4 found. Try downloading manually.")
            return

        console_res = live_stdout_run("ytdlp", self.url, "-o", f"ytdl-temp.{self.file_type}", "-f",
                                      f"{m4a_format}+{hd_mp4_format}")

        if console_res.returncode != 0:
            return

        self.save_file("download")


if __name__ == '__main__':

    downloader = Downloader()
    while True:
        downloader.main()
        print()

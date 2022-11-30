from os import remove
from os import replace
from subprocess import PIPE
from subprocess import Popen
from subprocess import run
from sys import stdout
from tkinter import Tk
from tkinter import filedialog

from eyed3 import load as eyed3_load


def live_run(*cmd):

    print()
    process = Popen(cmd, stdout=PIPE, shell=True)
    for c in iter(lambda: process.stdout.read(1), b""):
        stdout.buffer.write(c)
    process.wait()
    print()

    return process


def main():

    tk = Tk()
    tk.attributes("-topmost", True)
    tk.withdraw()

    url = input(">>> YouTube Video URL: ")
    file_type = input(">>> File Type (mp3/mp4): ")
    temp_file = f"ytdl-temp.{file_type}"

    if file_type == "mp3":

        res = live_run("ytdlp", url, "-o", temp_file, "-x", "--audio-format", "mp3")

        if res.returncode != 0:
            return

        name = input(">>> Music Title: ")
        album = input(">>> Music Album: ")
        artist = input(">>> Music Artist: ")

        metadata = eyed3_load(temp_file)
        metadata.tag.title = name
        metadata.tag.album = album
        metadata.tag.artist = artist
        metadata.tag.save()

        metadata.tag.images.set()

        fp = filedialog.asksaveasfilename(filetypes=[(file_type, f"*.{file_type}")],
                                          initialfile=name) + f".{file_type}"
        if fp != ".mp3":
            replace(temp_file, fp)
            print("(*) Completed")
        else:
            remove(temp_file)
            print("(*) Cancelled")

    elif file_type == "mp4":

        quality = input(">>> Video Quality (720/1080): ")
        if quality not in ("720", "1080"):
            print("(!) Invalid quality")

        if quality == "720":

            res = live_run("ytdlp", url, "-o", f"ytdl-temp.{file_type}", "-f", "mp4")
            if res.returncode != 0:
                return

        elif quality == "1080":

            res = run(("ytdlp", "-F", url), capture_output=True, shell=True)
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
                print("(!) No m4a found.")
                return
            if hd_mp4_format == "-1":
                print("(!) No 1920x1080 mp4 found.")
                return

            res = live_run("ytdlp", url, "-o", f"ytdl-temp.{file_type}", "-f", f"{m4a_format}+{hd_mp4_format}")
            if res.returncode != 0:
                return

        fp = filedialog.asksaveasfilename(filetypes=[(file_type, f"*.{file_type}")],
                                          initialfile="download") + f".{file_type}"
        if fp != ".mp4":
            replace(temp_file, fp)
            print("(*) Completed")
        else:
            remove(temp_file)
            print("(*) Cancelled")

    else:
        print("(!) Invalid file type")


if __name__ == '__main__':
    while True:
        main()
        print()

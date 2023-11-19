"""Everything related to youtube downloading."""
import datetime
import re
import os
import subprocess
from flask import send_file


AVAILABLE_FORMATS = ["3gp", "m4a", "mp3", "mp4", "webm"]
MEDIA_DIR = os.path.join(os.path.dirname(__file__), "Youtube")


def youtube_download(url, media_format):
    """
    Download content from youtube using yt-dlp.
    """
    # create media dir if not exsists
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)

    # test media format
    if media_format not in AVAILABLE_FORMATS:
        return {"error": "Invalid format"}, 400

    # test url with regex
    if not re.match(r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$", url):
        return {"error": "Invalid url"}, 400

    # used to later access the video
    identifier = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # create a dir named after identifier
    os.makedirs(os.path.join(MEDIA_DIR, identifier))

    # create a command to be run
    command = [
        "yt-dlp",
        "-P",
        os.path.join(MEDIA_DIR, identifier),
        "-o",
        "%(title)s.%(ext)s",
        url,
    ]

    # run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}, 500

    return {"message": "Downloaded successfully", "identifier": identifier}, 200


def youtube_serve(identifier):
    """
    Serve a youtube video.
    """
    # check if identifier is valid
    if not os.path.exists(os.path.join(MEDIA_DIR, identifier)):
        return {"error": "Invalid identifier"}, 400

    # get the file name
    file_name = os.listdir(os.path.join(MEDIA_DIR, identifier))[0]

    # return the file name
    return send_file(os.path.join(MEDIA_DIR, identifier, file_name), as_attachment=True)

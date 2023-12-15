"""Everything that has to do with downloading usign yt-dlp"""
import os
import random
import subprocess
import zipfile
from urllib.parse import quote

from flask import send_file

from backend.db import execute

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "downloaded-media")


FORMATS = {
    "1080p": [699, 399, 335, 303, 248, 299, 137],
    "720p": [698, 398, 334, 302, 247, 298, 136],
    "480p": [697, 397, 333, 244, 135],
    "360p": [696, 396, 332, 243, 134],
    "240p": [695, 395, 331, 242, 133],
    "144p": [694, 394, 330, 278, 160],
    "1440p": [700, 400, 336, 308, 271, 304, 264],
    "2K": [701, 401, 337, 315, 313, 305, 266],
    "4K": [402, 571, 272, 138],
    "mp3": ["ba[ext=m4a]/bestaudio"],
    "random": [""],
}


def get_size(path):
    size = os.path.getsize(path)
    if size < 1024:
        return f"{size} bytes"
    elif size < pow(1024, 2):
        return f"{round(size/1024, 2)} KB"
    elif size < pow(1024, 3):
        return f"{round(size/(pow(1024,2)), 2)} MB"
    elif size < pow(1024, 4):
        return f"{round(size/(pow(1024,3)), 2)} GB"


def download_to_server(url: str, format_str: str):
    """
    Downloads the content from the given url.
    Returns the media identifier if download is successful,
    else returns an error message and code.
    """
    if not url:
        return {"error": "url not provided"}, 400

    # check if url is not in the blacklist
    blacklist_urls = execute("SELECT url FROM blacklist", ())
    for x in [x[0] for x in blacklist_urls]:
        if x in quote(url):
            return {"error": "url is blacklisted"}, 403

    if format_str not in FORMATS:
        return {"error": "format not supported"}, 400

    # create the media dir if not exists
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)

    # make the identifier
    identifier = hex(hash(url + str(random.randint(1, 1000))))[3:]

    # create a dir named after identifier in the media dir
    os.makedirs(os.path.join(MEDIA_DIR, identifier))

    # create a command to be run
    command = [
        "yt-dlp",  # call yt-dlp
        "-P",  # set the output dir
        os.path.join(MEDIA_DIR, identifier),
        "-o",  # set the output file name
        "%(title)s.%(ext)s",
        "-f",  # set the format
        "/".join(map(str, FORMATS[format_str])) + "+bestaudio/best"
        if format_str != "random"
        else "bestvideo*+bestaudio/best",
        url,  # the url to download
    ]

    # create a command to extract playlist data
    playlist_command = [
        "yt-dlp",  # call yt-dlp
        "-P",  # set the output dir
        os.path.join(MEDIA_DIR, identifier),
        "--write-info-json",  # write media data to json file
        "--flat-playlist",  # ignore excess playlist metadata
        "--no-clean-info",
        url,  # the url to download
    ]

    # run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}, 500

    # check if downloaded media was a playlist
    if len(os.listdir(os.path.join(MEDIA_DIR, identifier))) > 1:
        try:
            subprocess.run(playlist_command, check=True)
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}, 500

    return {"identifier": identifier}, 200


def send_file_from_server(
    identifier: str, file_name_new: str | None = None, get_data_only: bool = False
):
    """Will send the file as an atachment to the client using the identifier"""
    # create the path to the file directory
    path = os.path.join(MEDIA_DIR, identifier)

    # check if the file directory exists
    if not os.path.exists(path):
        return {"error": "file not found"}, 404

    # check if multiple files were converted (a playlist)
    if len(os.listdir(path)) > 1:
        # change previously defined variables to fit playlist zip file
        for file in os.listdir(path):
            # find metadata file containing playlist title
            if file.split(".")[-1] == "json":
                file_name = file.rsplit(" [", maxsplit=1)[0] + ".zip"
        file_extention = "zip"
        zipfile_path = os.path.join(path, file_name)
        # create a zip file containing all converted playlist content
        with zipfile.ZipFile(zipfile_path, "w") as zip_object:
            for file in os.listdir(path):
                # ignore created .zip and json files
                if file.split(".")[-1] != "zip" and file.split(".")[-1] != "json":
                    zip_object.write(os.path.join(path, file), file)
            zip_object.close()

    else:
        # get the file name from the directory
        file_name = os.listdir(path)[0]

        file_extention = file_name.split(".")[-1]

    if get_data_only:
        return {
            "file_name": file_name.replace("." + file_extention, ""),
            "file_extention": file_extention,
            "file_size": get_size(os.path.join(path, file_name)),
        }, 200

    # create the path to the file
    path = os.path.join(path, file_name)

    # return the file as an attachment
    return send_file(
        path,
        as_attachment=True,
        download_name=file_name_new + "." + file_extention
        if file_name_new
        else file_name,
    )

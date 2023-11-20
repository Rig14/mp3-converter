"""Everything that has to do with downloading usign yt-dlp"""
import os
import subprocess

from flask import send_file

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "downloaded-media")


def download_to_server(url: str):
    """
    Downloads the content from the given url.
    Returns the media identifier if download is successful,
    else returns an error message and code.
    """
    # create the media dir if not exists
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)

    # make the identifier
    identifier = hex(hash(url))[3:]

    # create a dir named after identifier in the media dir
    try:
        os.makedirs(os.path.join(MEDIA_DIR, str(identifier)))
    except FileExistsError:
        return {"identifier": identifier}, 200

    # create a command to be run
    command = [
        "yt-dlp",  # call yt-dlp
        "-P",  # set the output dir
        os.path.join(MEDIA_DIR, identifier),
        "-o",  # set the output file name
        "%(title)s.%(ext)s",
        url,  # the url to download
    ]

    # run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}, 500

    return {"identifier": identifier}, 200


def send_file_from_server(identifier: str, file_name: str | None = None):
    """Will send the file as an atachment to the client using the identifier"""
    # create the path to the file directory
    path = os.path.join(MEDIA_DIR, identifier)

    # check if the file directory exists
    if not os.path.exists(path):
        return {"error": "file not found"}, 404

    # get the file name from the directory
    file_name = os.listdir(path)[0]

    # create the path to the file
    path = os.path.join(path, file_name)

    # return the file as an attachment
    return send_file(path, as_attachment=True, download_name=file_name)

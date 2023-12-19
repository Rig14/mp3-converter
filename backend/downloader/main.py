"""Everything that has to do with downloading usign yt-dlp"""
import os
import random
import shutil
import subprocess
import time
import zipfile
from urllib.parse import quote

from flask import send_file

from backend.db import execute

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "downloaded-media")
TTL = 60 * 60  # 1 hour

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


def get_size(path, is_dir=False):
    if is_dir:
        files = os.listdir(path)
        size = sum([os.path.getsize(os.path.join(path, x)) for x in files])
    else:
        size = os.path.getsize(path)
    if size < 1024:
        return f"{size} bytes"
    elif size < pow(1024, 2):
        return f"{round(size/1024, 2)} KB"
    elif size < pow(1024, 3):
        return f"{round(size/(pow(1024,2)), 2)} MB"
    elif size < pow(1024, 4):
        return f"{round(size/(pow(1024,3)), 2)} GB"


def download_metadata_file(path: object, url: str):
    # create a dir for metadata file
    os.makedirs(os.path.join(path, "metadata"))

    # create a command to extract playlist data
    playlist_command = [
        "yt-dlp",  # call yt-dlp
        "-P",  # set the output dir
        os.path.join(path, "metadata"),
        "--write-info-json",  # write media data to json file
        "--flat-playlist",  # ignore excess playlist metadata
        "--no-clean-info",
        url,  # the url to download
    ]

    # run the command
    try:
        subprocess.run(playlist_command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}, 500


def get_data_only_function(identifier):
    # create necessary paths
    path = os.path.join(MEDIA_DIR, identifier)
    media_files_path = os.path.join(path, "media_files")

    # check if the file directory exists
    if not os.path.exists(media_files_path):
        return {"error": "file not found"}, 404

    media_files_dict = {}
    # create a dictionary containing file data for each file in media_files dir
    for i, filename in enumerate(os.listdir(media_files_path)):
        file_data_dict = {
            "file_name": filename.split(".")[0],
            "file_extension": "." + filename.split(".")[-1],
            "file_size": get_size(os.path.join(media_files_path, filename))
            # "new_filename": None  would enable filename changing in custom selection
        }
        # add created dict to media_files_dict
        media_files_dict[i] = file_data_dict

    playlist_data_dict = {}

    # create a dictionary containing playlist data
    if len(media_files_dict.keys()) > 1:
        # extract playlist title from metadata file's filename
        metadata_file = os.listdir(os.path.join(path, "metadata"))[0]
        playlist_data_dict["title"] = metadata_file.rsplit(" [", maxsplit=1)[0]

        # get size of the whole playlist (media_files dir)
        playlist_data_dict["size"] = get_size(media_files_path, True)
        playlist_data_dict["extension"] = ".zip"

    return {
        "files_data": media_files_dict,
        # "is_playlist": is_playlist
        "playlist_data": playlist_data_dict,
    }


"""
    return {
        "file_name": file_name.replace("." + file_extension, ""),
        "file_extension": "." + file_extension,
        "file_size": get_size(os.path.join(path, file_name)),
    }, 200
"""


def zip_playlist(playlist_path: object, url: str):
    """
    Extracts playlist title with yt-dlp command.
    Moves all media files to a single zip file named after playlist title.
    Deletes all files except zip file.
    :param path: path to the playlist media files folder (MEDIA_DIR + identifier)
    :param url: url of the converted playlist
    """
    # list of media files in playlist, might be used for playlist-custom-selection
    media_files = os.listdir(playlist_path)

    zipfile_name = "zipped-playlist.zip"  # hardcoded filename
    new_filename = ""  # playlist title
    zipfile_path = os.path.join(playlist_path, zipfile_name)

    # move all playlist media to newly created zip file
    with zipfile.ZipFile(zipfile_path, "w") as zip_object:
        # process and delete all files except .zip file
        for file in os.listdir(playlist_path):
            file_path = os.path.join(playlist_path, file)
            if file in media_files:
                zip_object.write(file_path, file)
                os.remove(file_path)
            elif file.split(".")[-1] == "json":
                # extract playlist title from metadata file filename
                new_filename = file.rsplit(" [", maxsplit=1)[0] + ".zip"
                os.remove(file_path)
        zip_object.close()

    # replace hardcoded zipfile name with playlist title
    if new_filename:
        os.rename(zipfile_path, os.path.join(playlist_path, new_filename))


def download_to_server(url: str, format_str: str):
    """
    Downloads the content from the given url.
    Returns the media identifier if download is successful,
    else returns an error message and code.
    """
    # check media folder for old files and delete them
    for file in os.listdir(MEDIA_DIR):
        file_path = os.path.join(MEDIA_DIR, file)
        if os.path.isdir(file_path):
            if len(os.listdir(file_path)) == 0:
                shutil.rmtree(file_path)
            else:
                if os.path.getmtime(file_path) < time.time() - TTL:
                    shutil.rmtree(file_path)

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

    # create a dir for all downloaded media files
    os.makedirs(os.path.join(MEDIA_DIR, identifier, "media_files"))

    # create a command to be run
    command = [
        "yt-dlp",  # call yt-dlp
        "-P",  # set the output dir
        os.path.join(MEDIA_DIR, identifier, "media_files"),
        "-o",  # set the output file name
        "%(title)s.%(ext)s",
        "-f",  # set the format
        "/".join(map(str, FORMATS[format_str])) + "+bestaudio/best"
        if format_str != "random"
        else "bestvideo*+bestaudio/best",
        url,  # the url to download
    ]

    # run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}, 500

    # check if downloaded media was a playlist
    if len(os.listdir(os.path.join(MEDIA_DIR, identifier, "media_files"))) > 1:
        download_metadata_file(os.path.join(MEDIA_DIR, identifier), url)

    return {"identifier": identifier}, 200


def send_file_from_server(
    identifier: str,
    file_name_new: str | None = None,
    get_data_only: bool = False,
    selected: str | None = None,
):
    """Will send the file as an atachment to the client using the identifier"""
    # create the path to the file(s) directory
    path = os.path.join(MEDIA_DIR, identifier)

    # check if the file directory exists
    if not os.path.exists(path):
        return {"error": "file not found"}, 404

    if get_data_only:
        return get_data_only_function(identifier)

    # get the file name from the directory
    file_name = os.listdir(path)[0]

    file_extension = file_name.split(".")[-1]

    if get_data_only:
        return {
            "file_name": file_name.replace("." + file_extension, ""),
            "file_extension": "." + file_extension,
            "file_size": get_size(os.path.join(path, file_name)),
        }, 200

    # create the path to the file
    path = os.path.join(path, file_name)

    # return the file as an attachment
    return send_file(
        path,
        as_attachment=True,
        download_name=file_name_new + "." + file_extension
        if file_name_new
        else file_name,
    )

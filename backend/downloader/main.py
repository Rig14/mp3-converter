"""Everything that has to do with downloading usign yt-dlp"""
import os
import random
import shutil
import subprocess
import time
import zipfile
import json
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
    media_dir_path = os.path.join(path, "media_files")

    # check if the file directory exists
    if not os.path.exists(media_dir_path):
        return {"error": "file not found"}, 404

    media_files_dict = {}
    # create a dictionary containing file data for each file in media_files dir
    for i, filename in enumerate(os.listdir(media_dir_path)):
        file_data_dict = {
            "file_name": filename.rsplit(".", maxsplit=1)[0],
            "file_extension": "." + filename.rsplit(".", maxsplit=1)[-1],
            "file_size": get_size(os.path.join(media_dir_path, filename)),
            # "new_filename": "",
        }
        # add created dict to media_files_dict
        media_files_dict[i] = file_data_dict

    playlist_data_dict = {}

    # create a dictionary containing playlist data
    if len(media_files_dict.keys()) > 1:
        # extract playlist title from metadata file's filename
        metadata_file = os.listdir(os.path.join(path, "metadata"))[0]

        playlist_data_dict["title"] = metadata_file.rsplit(" [", maxsplit=1)[0]
        playlist_data_dict["file_size"] = get_size(media_dir_path, True)  # whole dir
        playlist_data_dict["file_extension"] = ".zip"
        playlist_data_dict["selected"] = []
        # playlist_data_dict["new_title"] = ""

    return {
        "files_data": media_files_dict,
        "playlist_data": playlist_data_dict,
    }, 200


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
    os.makedirs(
        os.path.join(MEDIA_DIR, identifier, "media_files")
    )  # 2 dirs at once possible?

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

    # path to downloaded media dir
    path = os.path.join(MEDIA_DIR, identifier)

    # check if downloaded media was a playlist
    if len(os.listdir(os.path.join(path, "media_files"))) > 1:
        download_metadata_file(path, url)

    return {"identifier": identifier}, 200


def zip_playlist(path: object, selected: list):
    """
    Move all elected playlist content to file "zipped-playlist.zip".
    :param path: path to the playlist media files folder (MEDIA_DIR + identifier)
    :param url: url of the converted playlist
    """
    # hardcoded filename
    zipfile_name = "zipped-playlist.zip"

    # create paths
    zipfile_dir_path = os.path.join(path, "zip_file")
    media_dir_path = os.path.join(path, "media_files")
    zipfile_path = os.path.join(zipfile_dir_path, zipfile_name)

    # remove previously created zip file | create new dir if first download
    if os.path.isdir(zipfile_dir_path):
        # stored zipfile name is constant, only downloaded file's name changes
        os.remove(zipfile_path)
    else:
        os.makedirs(zipfile_dir_path)

    # list of stored media filenames with extension
    media_files = os.listdir(media_dir_path)

    # move selected playlist media to zipfile
    with zipfile.ZipFile(zipfile_path, "w") as zip_object:
        for i in selected:
            media = media_files[int(i)]  # example: song.mp3
            z_path = os.path.join(media_dir_path, media)
            zip_object.write(z_path, media)
        zip_object.close()

    # extract playlist title from metadata file's filename  (should find a better way)
    metadata_file = os.listdir(os.path.join(path, "metadata"))[0]
    old_filename = metadata_file.rsplit(" [", maxsplit=1)[0]

    return zipfile_path, old_filename


def send_file_from_server(
    identifier: str,
    selected: str,
    new_filename: str,
    get_data_only: bool = False,
):
    """Will send the file as an atachment to the client using the identifier"""
    if new_filename == ".":
        new_filename = ""

    # create the path to the file(s) directory
    path = os.path.join(MEDIA_DIR, identifier)

    # check if the file directory exists
    if not os.path.exists(path):
        return {"error": "file not found"}, 404

    if get_data_only:
        return get_data_only_function(identifier)

    # get selected files
    selected = selected.split(".")

    # return selected playlist content as a zipfile
    if len(selected) > 1:
        # path to zip file containing all selected media, playlist title
        zipfile_path, old_filename = zip_playlist(path, selected)

        return send_file(
            zipfile_path,
            as_attachment=True,
            download_name=new_filename + ".zip"
            if old_filename != new_filename and new_filename != ""
            else old_filename + ".zip",
        )

    # return the single media file as an attachment
    elif len(selected) == 1:
        # list of stored media filenames with extension
        media_dir_path = os.path.join(path, "media_files")

        # list of stored media filenames with extension
        media_files = os.listdir(media_dir_path)

        # file index in media_files dir
        index = int(selected[0])

        # get file data from media_files dir
        old_filename = media_files[index].rsplit(".", maxsplit=1)[0]
        file_extension = "." + media_files[index].rsplit(".", maxsplit=1)[-1]
        file_path = os.path.join(media_dir_path, old_filename + file_extension)

        # new_filename checking and logic might need rework in javascript processFormData()
        return send_file(
            file_path,
            as_attachment=True,
            download_name=new_filename + file_extension
            if old_filename != new_filename and new_filename != ""
            else old_filename + file_extension,
        )

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
TTL = 60 * 60 * 15  # 1 hour

hardcoded_data_dict = {
    "files_data": {
        "0": {
            "file_extension": ".m4a",
            "file_name": "A Liar's Funeral",
            "file_size": "5.06 MB",
            "new_filename": "",
        },
        "1": {
            "file_extension": ".m4a",
            "file_name": "All Out Life",
            "file_size": "5.25 MB",
            "new_filename": "",
        },
        "2": {
            "file_extension": ".m4a",
            "file_name": "Birth Of The Cruel",
            "file_size": "4.26 MB",
            "new_filename": "",
        },
        "3": {
            "file_extension": ".m4a",
            "file_name": "Critical Darling",
            "file_size": "5.96 MB",
            "new_filename": "",
        },
        "4": {
            "file_extension": ".m4a",
            "file_name": "Death Because of Death",
            "file_size": "1.25 MB",
            "new_filename": "",
        },
        "5": {
            "file_extension": ".m4a",
            "file_name": "Insert Coin",
            "file_size": "1.53 MB",
            "new_filename": "",
        },
        "6": {
            "file_extension": ".m4a",
            "file_name": "My Pain",
            "file_size": "6.3 MB",
            "new_filename": "",
        },
        "7": {
            "file_extension": ".m4a",
            "file_name": "Nero Forte",
            "file_size": "4.87 MB",
            "new_filename": "",
        },
        "8": {
            "file_extension": ".m4a",
            "file_name": "Not Long for This World",
            "file_size": "6.11 MB",
            "new_filename": "",
        },
        "9": {
            "file_extension": ".m4a",
            "file_name": "Orphan",
            "file_size": "5.58 MB",
            "new_filename": "",
        },
        "10": {
            "file_extension": ".m4a",
            "file_name": "Red Flag",
            "file_size": "3.89 MB",
            "new_filename": "",
        },
        "11": {
            "file_extension": ".m4a",
            "file_name": "Solway Firth",
            "file_size": "5.49 MB",
            "new_filename": "",
        },
        "12": {
            "file_extension": ".m4a",
            "file_name": "Spiders",
            "file_size": "3.76 MB",
            "new_filename": "",
        },
        "13": {
            "file_extension": ".m4a",
            "file_name": "Unsainted",
            "file_size": "4.03 MB",
            "new_filename": "",
        },
        "14": {
            "file_extension": ".m4a",
            "file_name": "What's Next",
            "file_size": "852.66 KB",
            "new_filename": "",
        },
    },
    "playlist_data": {
        "file_extension": ".zip",
        "file_size": "64.16 MB",
        "new_title": "SLIPKNOT - We Are Not Your Ki",
        "selected": "1.2.3.4.7.8.9.10.11.12",
        "title": "SLIPKNOT - We Are Not Your Kind (FULL ALBUM 2019)",
    },
}


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
            "file_size": get_size(os.path.join(media_files_path, filename)),
            "new_filename": "",
        }
        # add created dict to media_files_dict
        media_files_dict[i] = file_data_dict

    playlist_data_dict = {}

    # create a dictionary containing playlist data
    if len(media_files_dict.keys()) > 1:
        # extract playlist title from metadata file's filename
        metadata_file = os.listdir(os.path.join(path, "metadata"))[0]
        playlist_data_dict["title"] = metadata_file.rsplit(" [", maxsplit=1)[0]
        playlist_data_dict["new_title"] = ""

        # get size of the whole playlist (media_files dir)
        playlist_data_dict["file_size"] = get_size(media_files_path, True)
        playlist_data_dict["file_extension"] = ".zip"
        playlist_data_dict["selected"] = []

    return {
        "files_data": media_files_dict,
        "playlist_data": playlist_data_dict,
        # "is_playlist": is_playlist
    }, 200


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
    data_dict: str | None = None,
    get_data_only: bool = False,
):
    """Will send the file as an atachment to the client using the identifier"""
    # create the path to the file(s) directory
    path = os.path.join(MEDIA_DIR, identifier)

    # check if the file directory exists
    if not os.path.exists(path):
        return {"error": "file not found"}, 404

    # if get_data_only:
    #    return get_data_only_function(identifier)

    # data_dict = json.loads(data_dict)
    data_dict = hardcoded_data_dict
    identifier = "477904aa0dbb81f"

    # return the single media file as an attachment
    if len((data_dict["files_data"]).keys()) == 1:  # add checking selected for short PL
        # get file data from data_dict
        old_filename = data_dict["files_data"]["0"]["file_name"]
        new_filename = data_dict["files_data"]["0"]["new_filename"]
        file_extension = data_dict["files_data"]["0"]["file_extension"]
        file_path = os.path.join(path, "media_files", old_filename + file_extension)

        # new_filename checking and logic might need rework in javascript processFormData()
        return send_file(
            file_path,
            as_attachment=True,
            download_name=new_filename + file_extension
            if old_filename != new_filename and new_filename != ""
            else old_filename + file_extension,
        )
    else:
        # create path for zip file directory
        zipfile_dir = os.path.join(path, "zip_file")

        # remove previously created zip file | create new dir when first download
        if os.path.isdir(zipfile_dir):
            os.remove(os.path.join(zipfile_dir, os.listdir(zipfile_dir)[0]))
        else:
            os.makedirs(zipfile_dir)

        zipfile_name = "zipped-playlist.zip"  # hardcoded filename
        zipfile_path = os.path.join(zipfile_dir, zipfile_name)

        selected_indexes = data_dict["playlist_data"]["selected"].split(".")

        # move all playlist media to newly created zip file
        with zipfile.ZipFile(zipfile_path, "w") as zip_object:
            for i in selected_indexes:
                media = data_dict["files_data"][i]
                filename = media["file_name"]
                z_path = os.path.join(
                    path, "media_files", filename + media["file_extension"]
                )
                zip_object.write(
                    z_path, filename + media["file_extension"]
                )  # could add new name from html form
            zip_object.close()

        # replace hardcoded zipfile name with playlist title
        old_title = data_dict["playlist_data"]["title"]
        new_title = data_dict["playlist_data"]["new_title"]

        return send_file(
            zipfile_path,
            as_attachment=True,
            download_name=new_title + ".zip"
            if old_title != new_title and new_title != ""
            else old_title + ".zip",
        )


""" previous version
    # return the file as an attachment
    return send_file(
        path,
        as_attachment=True,
        download_name=file_name_new + "." + file_extension
        if file_name_new
        else file_name,
    )
"""

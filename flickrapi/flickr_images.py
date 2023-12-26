# -*- coding: utf-8 -*-
"""Web scraping using Flickr API.
This is a scraping sample using Flickr API.
Flickr is a web site to share a lot of kind of photos.
If you use Flickr API, you can do scraping and get photos from Flickr.
You have to ready API key and secret from Flickr to run this module.
Please write API key and secret into api_key.yaml.
And also, please specify target of photo category and number of download photos
when you running this module.

Example:
    $ python flickr_images.py [target] [number of photos]
"""
import os
import shutil
import sys
import time
import urllib.request

import yaml
from flickrapi import FlickrAPI


def main():
    """Web scraping main function.
    Scraping using Flickr API and download photos of target.
    Downloaded photos are saved in images/ directory.
    :return:
    """
    # get API Key from yaml
    key = ""
    secret = ""
    try:
        with open("api_key.yaml", "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            key = data["API_KEY"]["key"]
            secret = data["API_KEY"]["secret"]
    except FileNotFoundError:
        print("api_key.yaml does not exists.")
        exit()

    # check argument if specify target animal
    target = ""
    per_page = 0
    try:
        target = sys.argv[1]
        per_page = int(sys.argv[2])
    except IndexError:
        print("Please specify target(str) and number of images(int).")
        exit()
    except ValueError:
        print("Please specify target(str) and number of images(int).")
        exit()

    # make target directory (if it's exist, remove and remake directory)
    save_dir = f"images/{target}"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        shutil.rmtree(save_dir)
        os.makedirs(save_dir)

    # call FlickrAPI
    try:
        flickr = FlickrAPI(api_key=key, secret=secret, format="parsed-json")
        response = flickr.photos.search(
            text=target,
            per_page=per_page,
            media="photos",
            sort="relevance",
            safe_search=1,
            extras="url_q, licence",
        )
    except Exception:
        print("Occured any connection error.")
        exit()

    # get images from API response
    wait_time = 1
    for image in response["photos"]["photo"]:
        save_file = f"{save_dir}/{image['id']}.jpg"
        if os.path.exists(save_file):
            continue
        with urllib.request.urlopen(image["url_q"]) as u:
            data = u.read()
        with open(save_file, "wb") as f:
            f.write(data)
        time.sleep(wait_time)


if __name__ == "__main__":
    main()

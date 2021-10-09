import os
import shutil
import sys
import time
import urllib.request

import yaml
from flickrapi import FlickrAPI

# get API Key from yaml
key = ''
secret = ''
try:
    with open('api_key.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        key = data['API_KEY']['key']
        secret = data['API_KEY']['secret']
except FileNotFoundError as e:
    print(e)
    exit()

# check argument if specify target animal
target = ''
per_page = 0
try:
    target = sys.argv[1]
    per_page = int(sys.argv[2])
except IndexError:
    print('Please specify target(str) and number of images(int).')
    exit()
except ValueError:
    print('Please specify target(str) and number of images(int).')
    exit()

# make target directory (if it's exist, remove and remake directory)
save_dir = 'images/' + target
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
else:
    shutil.rmtree(save_dir)
    os.makedirs(save_dir)

# call FlickrAPI
flickr = FlickrAPI(api_key=key, secret=secret, format='parsed-json')
response = flickr.photos.search(
    text=target,
    per_page=per_page,
    media='photos',
    sort='relevance',
    safe_search=1,
    extras='url_q, licence'
)

# get images from API response
wait_time = 1
for image in response['photos']['photo']:
    save_file = save_dir + '/' + image['id'] + '.jpg'
    if os.path.exists(save_file):
        continue
    data = urllib.request.urlopen(image['url_q']).read()
    with open(save_file, 'wb') as f:
        f.write(data)
    time.sleep(wait_time)
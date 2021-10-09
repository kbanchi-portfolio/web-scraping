import sys

from bs4 import BeautifulSoup
import requests

# read all categories from list file
all_categories_list = './zeroichi_media.list'
all_categories = []
with open(all_categories_list, 'r') as f:
    all_categories = f.read().split('\n')

# check if target category in all categories and set target category
target_category = ''
try:
    target_category = sys.argv[1]
    if not target_category in all_categories:
        print('Please specify target category from the following.')
        print('-- target categories --')
        for category in all_categories:
            print(category, end=' / ')
        exit()
except IndexError:
    print('Please specify target category argument from the following.')
    print('-- target categories --')
    for category in all_categories:
        print(category, end=' / ')
    exit()

# set scraping url
BASE_URL = 'https://zeroichi.media'
url = BASE_URL + '/category/' + target_category

# open url and get response
response = requests.get(url)
text = response.text

# parse text to html
soup = BeautifulSoup(text, 'html.parser')

# get and print archive post list
archives = soup.select('.archive-post')
for archive in archives:
    published = archive.find('time',class_='published')
    title = archive.find('h2', class_='entry-title')
    print(published.text + " : " + title.text)
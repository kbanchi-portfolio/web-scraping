# -*- coding: utf-8 -*-
"""Web scraping using Selenium.
This is a scraping sample using Selenium.
This is scarping prcm.
Please specify target category and number of photos
when running this module.

Example:
    $ python prcm.py [target] [number of photos]
"""
import os
import shutil
import sys
import time
import urllib.request

from selenium import webdriver

# set url
BASE_URL = "https://prcm.jp"


def main():
    """Web scraping main function
    Scraping using Selenium and download photos of target.
    Downloaded photos are saved in images/ directory.
    :return:
    """
    # check argument and set target text
    target = ""
    per_page = 0
    try:
        target = sys.argv[1]
        per_page = int(sys.argv[2])
    except IndexError:
        print("Please specify target text(str) and number of page(int).")
        exit()
    except ValueError:
        print("Please specify target text(str) and number of page(int).")
        exit()

    # set save directory
    save_dir = f"images/{target}"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    else:
        shutil.rmtree(save_dir)
        os.mkdir(save_dir)

    # set selenium driver and access page
    driver = webdriver.Firefox()
    wait_time = 1
    try:
        # access top page and search by target string
        driver.get(BASE_URL)
        driver.find_element_by_css_selector(".search__input").send_keys(target)
        driver.find_element_by_css_selector(".search__btn").click()
        time.sleep(wait_time)
        # access list pages and get images
        for i in range(per_page):
            image_list = driver.find_element_by_id(
                "imglist_container"
            ).find_elements_by_class_name("list-pic__item")
            for image in image_list:
                image_url = image.find_element_by_css_selector(
                    "a > div > img"
                ).get_attribute("src")
                file_path = f"{save_dir}/{image_url.split('/')[-1]}"
                data = urllib.request.urlopen(image_url).read()
                with open(file_path, "wb") as f:
                    f.write(data)
            # access to next page
            page_navigation = driver.find_element_by_class_name("page-navigation")
            next_link = page_navigation.find_element_by_class_name(
                "page-navigation__next"
            )
            link_url = next_link.find_element_by_css_selector("a").get_attribute("href")
            driver.get(link_url)
            time.sleep(wait_time)
    except Exception as e:
        print("Cause Exception...", e)
        driver.quit()
        exit()
    finally:
        # close driver
        driver.quit()


if __name__ == "__main__":
    main()

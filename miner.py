#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import random, sys
import time


def main(argv=None):
    if argv is None:
        argv = sys.argv

    EMAIL = argv[2]
    PASSWORD = argv[3]

    # Dependencies
    chromeDriverLocation = "./chromedriver"
    driver = webdriver.Chrome(chromeDriverLocation)
    words = [line.strip() for line in open("wordsenglish.txt")] # delete later

    # login
    driver.get("https://login.live.com/")
    emailbox = driver.find_element_by_id("i0116")
    emailbox.send_keys(EMAIL)
    emailbox.send_keys(Keys.RETURN)

    # wait for next textbox to show up
    time.sleep(5)
    passwordbox = driver.find_element_by_id("i0118")
    passwordbox.send_keys(PASSWORD)
    passwordbox.send_keys(Keys.RETURN)

    time.sleep(5)

    driver.get("http://www.bing.com")

    for i in range(0,int(argv[1])):
        search_box = driver.find_element_by_id("sb_form_q")
        search_box.clear()
        search_box.send_keys(random.choice(words))
        search_box.send_keys(Keys.RETURN)

        # wait a few seconds
        time.sleep(3)

if __name__ == "__main__":
    main()

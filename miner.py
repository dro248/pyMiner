#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import random, sys

def main(argv=None):
    if argv is None:
        argv = sys.argv

    words = [line.strip() for line in open("wordsenglish.txt")]
    chromeDriverLocation = "./chromedriver"
    driver = webdriver.Chrome(chromeDriverLocation)
    driver.get("http://www.bing.com")

    for i in range(0,int(argv[1])):
        search_box = driver.find_element_by_id("sb_form_q")
        search_box.clear()
        search_box.send_keys(random.choice(words))
        search_box.send_keys(Keys.RETURN)

if __name__ == "__main__":
    main()

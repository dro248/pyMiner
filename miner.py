#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import random, sys
import time
import argparse
import logging

# for debugging --> use bp() as breakpoint
from pdb import set_trace as bp

def parse_options():
    parser = argparse.ArgumentParser(prog="pyMiner", description="Searches BING with your account!", add_help=True)
    parser.add_argument("-n", "--number", action="store", type=int, help="The number of searches to do.", default=10)
    parser.add_argument("-e", "--email", action="store", help="Microsoft Live account email", required=True)
    parser.add_argument("-p", "--password", action="store", help="Account Password", required=True)
    return parser.parse_args()

def get_current_points(myDriver):
    try:
		pointsElement = WebDriverWait(myDriver, 50)\
			.until(EC.presence_of_element_located((By.ID, "id_rc")))

		points = pointsElement.get_attribute("innerHTML")
		print "you have", points, "points"
		return int(points)
    except:
		print "Error: points not found!"    
    


def main(argv=None):
    args = parse_options()

    EMAIL = args.email
    PASSWORD = args.password

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
    time.sleep(3)
    passwordbox = driver.find_element_by_id("i0118")
    passwordbox.send_keys(PASSWORD)
    passwordbox.send_keys(Keys.RETURN)

    # time.sleep(5)

    driver.get("http://www.bing.com")
    
    # get current number of points
    # print "getting current number of points..."
    current_pts = get_current_points(driver)

    for i in range(0,int(args.number)):
        search_box = driver.find_element_by_id("sb_form_q")
        search_box.clear()
        search_box.send_keys(random.choice(words))
        search_box.send_keys(Keys.RETURN)

        # wait a random number of seconds
        time.sleep(random.randint(2,6))

        new_pts = get_current_points(driver)
        if new_pts == current_pts:
        	print "No points gained with latest search.\nQuitting..."
        	break
        else:
        	current_pts = new_pts

if __name__ == "__main__":
    main()

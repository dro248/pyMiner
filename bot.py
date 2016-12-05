from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import random, sys
import time
import logging

import stats
from pdb import set_trace as bp

class Bot():
    def __init__(self, show=False):
        self.driver = None
        self.show = show
        self.chromeDriverLocation = "./chromedriver"
        self.words = [line.strip() for line in open("wordsenglish.txt")]
        if not self.show:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()
        else: self.display = None
        self.current_pts = 0

    def finish(self):
        """ Cleanup the driver and display """
        self.driver.close()
        if self.display is not None:
            self.display.stop()

    def mobile(self):
        """ Set the driver to the mobile version """
        self.driver = webdriver.Chrome(self.chromeDriverLocation)
        opts = Options()
        opts.add_argument("user-agent='Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>)" +
            " AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'")
        opts.add_argument("--disable-javascript")
        self.driver = webdriver.Chrome(self.chromeDriverLocation, chrome_options=opts)

    def desktop(self):
        """ Set the driver to the desktop version """
        self.driver = webdriver.Chrome(self.chromeDriverLocation)

    def desktop_initial_points(self):
        """ Gets the points from the screen immediately following the login screen """
        self.current_pts = int(self.driver.find_element_by_class_name("primary-text").get_attribute("innerHTML"))
        return self.current_pts

    def login(self, EMAIL, PASSWORD):
        self.driver.get("https://login.live.com/")
        emailbox = self.driver.find_element_by_id("i0116")
        emailbox.send_keys(EMAIL)
        emailbox.send_keys(Keys.RETURN)

        # wait for next textbox to show up
        time.sleep(1)
        passwordbox = self.driver.find_element_by_id("i0118")
        passwordbox.send_keys(PASSWORD)
        passwordbox.send_keys(Keys.RETURN)

    def bing(self):
        if self.driver is not None:
            self.driver.get("http://www.bing.com")

    def desktop_miner(self, data):
        """ Returns whether the points changed """
        search_box = self.driver.find_element_by_id("sb_form_q")
        search_box.clear()
        search_box.send_keys(random.choice(self.words))
        search_box.send_keys(Keys.RETURN)

        new_pts = self.get_current_points("id_rc")
        data.round(new_pts)
        if new_pts == self.current_pts:
            logging.info("No points gained with latest search.\n")
            return False
        elif new_pts < self.current_pts:
            logging.warn("Points decreased somehow: old: %s new: %s" % (str(self.current_pts), str(new_pts)))
            data.decrease(new_pts)
        else:
            data.increase(new_pts)
            self.current_pts = new_pts
        return True

    def mobile_miner(self, data):
        """ Returns whether the points changed """
        try:
            search_box = self.driver.find_element_by_id("sb_form_q")
            search_box.clear()
            search_box.send_keys(random.choice(self.words))
            search_box.send_keys(Keys.RETURN)
        except Exception as ex:
            logging.info("Caught GPS alert")
            self.driver.get("http://www.bing.com")
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return True

        new_pts = self.get_current_points("fly_id_rc")
        data.round(new_pts)
        if new_pts == self.current_pts:
            logging.warn("No points gained with latest search.\nQuitting...")
            return False
        elif new_pts < self.current_pts:
            logging.warn("Points decreased somehow: old: %s new: %s" % (str(self.current_pts), str(new_pts)))
            data.decrease(new_pts)
        else:
            data.increase(new_pts)
            self.current_pts = new_pts
        return True

    def get_current_points(self, el_id):
        try:
            while True:
                pointsElement = WebDriverWait(self.driver, 20)\
                    .until(EC.presence_of_element_located((By.ID, el_id)))
                points = pointsElement.get_attribute("innerHTML")
                if not points.isdigit():
                    logging.info("waiting for points to load")
                    time.sleep(.5)
                    continue
                logging.info("you have %s points" % points)
                return int(points)
        except ValueError:
            logging.error("Issue converting value:[%s] to int." %  str(points))
            return 0


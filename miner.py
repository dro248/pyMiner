#!/usr/bin/env python

import argparse
import logging
import getpass
import random, time

from stats import Stats
from bot import Bot
from pdb import set_trace as bp

def parse_options():
    parser = argparse.ArgumentParser(prog="pyMiner", description="Searches BING with your account!", add_help=True)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug level logging. A toooon of stuff from selenium gets logged btw.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable info level logging")
    parser.add_argument("-n", "--number", action="store", type=int, help="The number of searches to do.", default=100)
    parser.add_argument("-e", "--email", action="store", help="Microsoft Live account email", required=True)
    parser.add_argument("-p", "--password", action="store", help="Account Password")
    parser.add_argument("-j", "--json", action="store_true", help="Enables json output with process information for easy parsing after the fact")
    parser.add_argument("-s", "--show", action="store_true", help="Shows the display")
    return parser.parse_args()

def configure_output(args):
    """ Returns whether the program should create json output or do normal logging """
    if args.json:
        logging.basicConfig(level=logging.ERROR)
        return True
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARN)
    return False

def main():
    args = parse_options()
    store_info = configure_output(args)
    password = getpass.getpass() if args.password == None else args.password

    bot = Bot(args.show)
    logging.info("Desktop mode")
    bot.desktop()
    bot.login(args.email, password)

    data = Stats(store_info)
    data.start(bot.desktop_initial_points() or 0)
    data.set_title("Bing Desktop Browser")
    bot.bing()

    for i in range(0,args.number):
        if not bot.desktop_miner(data):
            break
        sleep_time = random.randint(5,15)
        logging.info("sleeping %i" % sleep_time)
        data.sleep(sleep_time)
        time.sleep(sleep_time)

    logging.info("Mobile mode")
    bot.mobile()
    bot.login(args.email, password)

    for i in range(0,args.number):
        if not bot.mobile_miner(data):
            break
        sleep_time = random.randint(5,15)
        logging.info("sleeping %i" % sleep_time)
        data.sleep(sleep_time)
        time.sleep(sleep_time)

    bot.finish()

    if store_info:
        print data.done()
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Caught Keyboard Interrupt. Exiting.")


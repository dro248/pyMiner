#!/usr/bin/env python

import argparse
import logging
import getpass
import random, time
import json
import traceback

from stats import Stats
from bot import Bot
from pdb import set_trace as bp

def parse_options():
    parser = argparse.ArgumentParser(prog="pyMiner", description="Searches BING with your account!", add_help=True)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug level logging. A toooon of stuff from selenium gets logged btw.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable info level logging")
    parser.add_argument("-n", "--number", action="store", type=int, help="The number of searches to do.", default=200)
    parser.add_argument("-e", "--email", action="store", help="Microsoft Live account email")
    parser.add_argument("-p", "--password", action="store", help="Account Password")
    parser.add_argument("-j", "--json", action="store_true", help="Enables json output with process information for easy parsing after the fact")
    parser.add_argument("-s", "--show", action="store_true", help="Shows the display")
    parser.add_argument("-w", "--words", action="store", help="The File of Search Terms", default="./wordsenglish.txt")
    parser.add_argument("-a", "--accounts", action="store", help="The file of user accounts")
    return parser.parse_args()

def configure_output(args):
    """ Returns whether the program should print json output or do normal logging """
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARN)
    return args.json

def getCredentials(account, args):
    email = account.get("email") or args.email or raw_input("Email: ")
    password = account.get("password") or args.password or getpass.getpass(prompt="Password for \"%s\": " % email)
    return (email, password)

def mine(args, store_info, data, account={}):
    """
    @param account json { email: "", password: ""}
    """
    email = ""
    password = ""

    email, password = getCredentials(account, args)

    if email == "" or password == "":
        logging.error("No Email or password provided")
        return

    bot = Bot(args.show, args.words)
    logging.info("Desktop mode")
    bot.desktop()
    bot.login(email, password)

    data.start(bot.desktop_initial_points() or 0, email)
    logging.info("Starting points: %i" % data.initial_points)
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
    bot.login(email, password)

    for i in range(0,args.number):
        if not bot.mobile_miner(data):
            break
        sleep_time = random.randint(5,15)
        logging.info("sleeping %i" % sleep_time)
        data.sleep(sleep_time)
        time.sleep(sleep_time)

    data.done()
    bot.finish()

def getaccounts(args):
    filename = args.accounts
    with open(filename) as accountfile:
        accountlist = json.loads(accountfile.read()).get("accounts")
        return accountlist

def main():
    args = parse_options()
    try:
        store_info = configure_output(args)
        data = Stats()
        if (args.accounts != None):
            accounts = getaccounts(args)
            for i,account in enumerate(accounts):
                mine(args, store_info, data, account)
        else:
            mine(args, store_info)
        if args.json:
            print data.get_json()
    except IOError:
        logging.error("bad account filename")
    except KeyboardInterrupt:
        logging.info("Caught Keyboard Interrupt. Exiting.")
    except Exception as e:
        logging.error("Error. Use -v for more details.")
        logging.info("Exception Message: %s" % traceback.format_exc())

if __name__ == "__main__":
    main()

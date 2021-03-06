#!/usr/bin/env python

"""
ScreenyPy - A CLI tool to take websites' screenshots.
"""
# imports
import sys, os, argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time, requests, json


# Browser Binary locations
CHROME_BIN = "/bin/chromium-browser"
FIREFOX_BIN = "/bin/firefox"

# Proxy List generated from pubproxy.com
PROXY_URL = "http://pubproxy.com/api/proxy?limit=3&format=txt&https=true&type=http&last_check=5&level=elite"
read_proxy = requests.get(PROXY_URL)

PROXY_LISTTXT = read_proxy.text
PROXY_LIST = PROXY_LISTTXT.splitlines()

# Test URL to be used in case of no user input
TEST_URL = "http://en.wikipedia.org/"

# Function to generate screenshots using Chormium
def shots_chromium(url):
    """
    Chromium function.
    Takes screenshots using Chromium.
    """
    ctr = 0
    for proxy in PROXY_LIST:
        ctr = ctr+1
        FILE_NAME = proxy.split(':')[0] + "_chromium" + str(ctr) + ".png"
        options = webdriver.ChromeOptions()

        # Browser Options
        options.binary_location = CHROME_BIN
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        options.add_argument('disable-gpu')
        options.add_argument('--proxy-server=%s' % proxy)

        driver = webdriver.Chrome(chrome_options=options)

        start_time = time.time()
        driver.get(url)
        print("--- screenshot " + proxy.split(':')[0] + "_chromium" + str(ctr) + ".png"  +  " generated in %s seconds ---" % (time.time() - start_time))
        driver.implicitly_wait(10)

        driver.get_screenshot_as_file(FILE_NAME)
        driver.quit()

# Function to generate screenshots using Firefox
def shots_firefox(url):
    """
    Firefox function.
    Takes screenshots using Firefox.
    """
    ctr = 0
    for proxy in PROXY_LIST:
        ctr = ctr+1
        FILE_NAME = proxy.split(':')[0] + "_firefox" + str(ctr) + ".png"

        # Browser Options
        options = Options()
        options.binary_location = FIREFOX_BIN
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        options.add_argument('disable-gpu')
        options.add_argument('--proxy-server=%s' % proxy)

        driver = webdriver.Firefox(firefox_options=options)

        start_time = time.time()
        driver.get(url)
        print("--- screenshot " + proxy.split(':')[0] + "_firefox" + str(ctr) + ".png"  +  " generated in %s seconds ---" % (time.time() - start_time))
        driver.implicitly_wait(10)

        driver.get_screenshot_as_file(FILE_NAME)
        driver.quit()

def main():
    """
    Main function.
    Checks command-line arguments and calls the relevant function.
    """

    cli_argparser = argparse.ArgumentParser(description='screenypy - A python script that generates screenshots of a website from various random locations.')
    cli_argparser.add_argument('-c', '--chrome',  help="Generates screenshots using Chromium", required=False)
    cli_argparser.add_argument('-f', '--firefox', help="Generates screenshots using Mozilla Firefox", required=False)

    if len(sys.argv)==1:
        cli_argparser.print_help()
        sys.exit(1)

    cli_args = cli_argparser.parse_args()

    print ("\nThe website will be test from the following IPs:\n")
    for proxy in PROXY_LIST:
        print (proxy)

    if (cli_args.chrome):
        print ("\nBrowser selected: Chromium\nGenerating screenshots using Chromium\n\n")
        shots_chromium(cli_args.chrome)
    elif (cli_args.firefox):
        print ("\nBrowser selected: Firefox\nGenerating screenshots using Firefox\n\n")
        shots_firefox(cli_args.firefox)
    else:
        print ("\nBrowser selected: None\nGenerating screenshots using Chromium AND Firefox\n\n")
        shots_chromium(TEST_URL)
        shots_firefox(TEST_URL)

if __name__ == '__main__':
    sys.exit(main())

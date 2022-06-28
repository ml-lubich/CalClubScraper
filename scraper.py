import requests
import re
import time
from pathlib import Path
from collections import Counter

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# INIT
CLEAR_LINE_CODE = "\033[2K"
URL = "https://callink.berkeley.edu/organizations"

# SELENIUM FEATURES TO FIND ELEMS
LOAD_MORE_BUTTON_XPATH = '//*[@id="react-app"]/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/button/div/div/span'
URL_ORG_DIV_XPATH = "/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/a"
PRTL_LINK_TO_PULL_TITLE_IMG_DATABASE_STR = "se-infra-imageserver2.azureedge.net"

# HELPER FUNCTS:
def display_progress(curr_num_posts, len_all_posts, curr_post_name=None):
    percent_done = ((curr_num_posts/len_all_posts)*100)//1
    if curr_post_name:
        print(percentage_done + " | " + curr_post_name, end="\r")
    else:
        print(percentage_done, end="\r")

def display_count(i):
    print(i)

def clear_out():
    print(CLEAR_LINE_CODE, end="\r")

# DRIVER CODE:
if __name__ == '__main__':
    print("Starting\n===")

    # INSTALL CHROMEDRIVER
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chromedriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chromedriver_service, options=chrome_options)
    driver.get(URL)

    print("Loading All Posts...")

    # LOAD ALL ELEMENTS          
    # get the inner element of the button which contains the distinctive text "Load More"
    inner_elem = driver.find_elements(by=By.XPATH, value='//span[text()=\'Load More\']')
    if len(inner_elem) > 1:
        raise('Something went wrong: detected multiple "Load More" buttons.')
    # get sole item from list
    inner_elem = inner_elem[0]
    # get grandparent of the inner element, this is the button
    load_more_button = inner_elem.find_elements(by=By.XPATH, value='../..')
    if len(load_more_button) > 1:
        raise('Something went wrong: detected multiple grandparents of the "Load More" button.')
    # get sole item from list
    load_more_button = load_more_button[0]

    # REPEATEDLY CLICK ON "LOAD MORE" TO FIND ALL THE LINKS
    while True:
        try:
            load_more_button.click()
            time.sleep(0.1)
        except Exception as e:
            print("Failed to load post", e)
            break

    print("Done!\n===")
    print("Getting all the links...\n===")

    # FIND HTML ELEMENTS (LINKS AND ORG TITLES):
    # skip the first three elements that contain 'organization'
    all_post_elems = driver.find_elements(by=By.XPATH, value='//a[contains(@href, \'organization\')]')[2:]
    all_title_elems = driver.find_elements(by=By.XPATH, value='//*[contains(@size, \'75\')]')

    all_title_elems = [x.get_attribute('alt') for x in all_title_elems]

    # NUMBER OF POSTS (FOR PROGRESS)
    print("Found", str(len(all_post_elems)), "total posts")

    email_pattern = re.compile(r"(((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W]))")

    # SETUP TO SCRAPE EACH CLUB
    emails = {}
    links = {}

    print("Going to all links...\n===")

    # GO TO EACH URL AND REGEX SEARCH FOR EMAIL
    num_posts = 0
    for elem in all_post_elems:
        link_elem = elem.get_attribute("href")

        post_title = all_title_elems[num_posts]

        link = requests.get(link_elem)

        matches = []
        # turn on multiline and verbose
        matches_per_club = [x[0] for x in email_pattern.findall(link.text, re.X|re.M)] 
        matches.append(matches_per_club)
        # only append to entry if the list is not empty
        if matches != []:
            emails[post_title] = matches_per_club
        links[post_title] = link_elem

        clear_out() 

        display_progress(curr_num_posts=num_posts,
                         len_all_posts=len(all_post_elems), curr_post_name=post_title)
        
        num_posts += 1

    # SAVE SCRAPED DATA PERSISTENTLY
    print("===\nSaving Data")
    df_emails = pd.DataFrame([links, emails])
    df_emails.to_csv("emails.csv")
    print("Saved!")

    # QUIT CHROME DRIVER
    print("===\nQuitting Chrome Driver")
    driver.quit()

    print("===\nAll Done! 😎\n")

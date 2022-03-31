# webscraper_email.py

from selenium import webdriver
from bs4 import BeautifulSoup


import requests
import re
from collections import Counter
import pandas as pd


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# INIT


CLEAR_LINE_CODE = "\033[2K"
URL = "https://callink.berkeley.edu/organizations"

# SELENIUM FEATURES TO FIND ELEMS


LOAD_MORE_BUTTON_XPATH = '//*[@id="react-app"]/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/button/div/div/span'
URL_ORG_DIV_XPATH = "/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/a"
PRTL_LINK_TO_PULL_TITLE_IMG_DATABASE_STR = "se-infra-imageserver2.azureedge.net"
driver = webdriver.Chrome('./chromedriver')
driver.get(URL)

# HELPER FUNCTS:


def display_progress(curr_num_post, len_all_posts, curr_post_name=None):
    percentage_done = str(((curr_num_post / len_all_posts) * 100) // 1) + "%"
    if curr_post_name:
        print(percentage_done + " | " + curr_post_name, end="\r")
    else:
        print(percentage_done, end="\r")


def clear_out():
    print(CLEAR_LINE_CODE, end="\r")


# OLD (DEPRECATED)
# def clear_out(print_with_name=False):
#     if print_with_name:
#         print(" " * 40, end="\r")
#     else:
#         print(" " * 5, end="\r")


# CODE:


print("Starting")
print("===")
print("Loading All Posts")

# LOAD ALL ELEMS
# while True:
#     try:
#         loadMoreButton = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
#         time.sleep(0.5)
#         loadMoreButton.click()
#         time.sleep(0.5)
#     except Exception as e:
#         print(e)
#         break

print("Done!")
print("===")
print("Getting all the links...")

# FIND HTML ELEMS (LINKS AND ORG TITLES):
all_post_elems = driver.find_elements_by_xpath(
    "//a[contains(@href, 'organization')]")[2:]

all_title_elems = driver.find_elements_by_xpath(
    "//*[contains(@size, '75')]")

all_title_elems = [x.get_attribute('alt') for x in all_title_elems]

# NUMBER OF POSTS --> FOR PROGRESS
len_all_posts = len(all_post_elems)
print("Found " + str(len_all_posts) + " total posts")
print("Done!")

email_regex = re.compile(r"(((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W]))")

# SETUP
emails_dict = {}
link_dict = {}
get_title_regex = re.compile(r".*\/organization\/(.+)")

# TODOs
# working on getting short descriptions
# get_desc_regex = re.compile("([A-Z]\w*\s+(\w+\s{0,3})+){,20}")

print("===")
print("Going to all links")
num_post = 0
for elem in all_post_elems:
    link_elem = elem.get_attribute("href")
    # found_title = get_title_regex.match(link_elem)
    # if found_title:
    #     post_title = found_title.group(1)
    # else:
    #     continue

    post_title = all_title_elems[num_post]

    r_link = requests.get(link_elem)

    # TODO
    # post_desc = ""
    # desc_driver_getter = webdriver.Chrome('./chromedriver')
    # desc_driver_getter.get(link_elem)
    # # post_desc_regex_obj = get_desc_regex.match(r_link.text)

    # all_desc_container_elems = desc_driver_getter.find_element_by_class_name(
    #     'bodyText-large userSupplied')
    # all_desc_elems = all_desc_container_elems.find_elements_by_xpath("//p")

    # desc_driver_getter.quit()
    # print(all_desc_container_elems)
    # print(all_desc_elems)
    # if post_desc_regex_obj:
    #     post_desc = post_desc_regex_obj.group(1)
    # else:
    #     pass

    # matched_regex_lst = [post_desc, link_elem] <-- use this instead of below matched_reg_lst assignment

    link_dict[post_title] = link_elem
    matched_regex_lst = []
    matched_regex_lst.append(
        [x[0] for x in email_regex.findall(r_link.text, re.X | re.M)])
    if matched_regex_lst:
        emails_dict[post_title] = matched_regex_lst
    else:
        pass
    clear_out()
    display_progress(curr_num_post=num_post,
                     len_all_posts=len_all_posts, curr_post_name=post_title)
    num_post += 1

print("Done!")

# SAVE SCRAPED DATA PERSISTENTLY
print("===")
print("Saving Data")
df_emails = pd.DataFrame([link_dict, emails_dict])
df_emails.to_csv("callink_emails.csv")
print("Done!")

# QUIT CHROME DRIVER
print("===")
print("Quitting Chrome Driver")
driver.quit()

print("===")
print("All Done! 😎\n")
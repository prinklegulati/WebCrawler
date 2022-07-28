import csv
import os
import re

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

"""As the page is to be crawled have multiple pages and are dynamic in nature,therefore only using beautifulsoup 
doesn't provide good solution, However, only using selenium can provide a solution but due to the nature of selenium 
that is as it is slower than that of beautifulsoup , we used selenium only where it is absolutely necessary """
from selenium.common.exceptions import WebDriverException,NoSuchElementException
# importing Selenium Exceptions , It will throw webdriverexception if the drivers downloaded for browser is of
# different version for example out Google Chrome installed has been updated but corresponding driver is not updated,
# in that case it won't be able to open chrome and no SuchElement exception if no element with specified attributes
# could be found
from collections import deque
# deque is special type of container where push and pop operation can be performed at both ends
import requests

"""importing requests in order to do operations on URL"""
from bs4 import BeautifulSoup
# As we are using BeautifulSoup along with selenium to increase the speed of scrapping
import time
from selenium.webdriver.support import expected_conditions as EC


class WebCrawler:
    baseURL = "https://pureportal.coventry.ac.uk"
    endpoint = "/en/organisations/coventry-university/persons"
    crawling_URL = baseURL + endpoint
    """ crawling_URL: This is the URL that is going to be crawled"""
    visited_list = deque()
    """visited list is a dequeue which will store all the URLs that will be crawled on first level"""
    author_url_list = []
    """author_url_list stores all the URL for all the authors crawled on first node"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver_path = 'C:\\Users\\Prinkle\\Downloads\\chromedriver_win321\\chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    def __init__(self):
        self.directory = "Scrapped_files"
        self.filename = self.directory + "/scrapped_data.csv"
        try:
            os.mkdir(self.directory)
        except OSError as e:
            print("Directory already exist")
        self.csv_writer = csv.writer(open(self.filename, "w", newline='', encoding="utf-8"))
        try:
            self.driver.get(self.crawling_URL)
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]'))).click()
            self.crawling(self.crawling_URL)
            print(self.visited_list)
            self.createcsv()
            while len(self.author_url_list):
                deepurl1=self.author_url_list.pop(0)
                print(deepurl1)
                self.depth_crawling(deepurl1)
        except Exception as e:
            raise WebDriverException("Unable to start Chrome")

    def crawling(self, weburl):
        self.visited_list.append(weburl)
        response = requests.get(weburl)
        plain_text = response.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for author_names in soup.findAll('h3', {'class': 'title'}):
            for author_hyperlink_tag in author_names.findAll('a'):
                author_hyperlink_name_span = author_hyperlink_tag.find('span')
                author_name = author_hyperlink_name_span.text
                # Author.append(Author_Name)
                print(author_name)
                author_url = author_hyperlink_tag.get('href')
                if author_url != "" or author_url != "#" or author_url != None:
                    self.author_url_list.append(author_url)
        try:
            time.sleep(10)
            next_page = self.driver.find_element_by_class_name("next")
            if (next_page.is_enabled()):
                time.sleep(5)
                next_page.click()
                time.sleep(5)
                webUrl = self.driver.current_url
                self.crawling(webUrl)
        except NoSuchElementException as e:
            print("No more pages")

    def depth_crawling(self,webpage_for_deep_crawling):
        baseurl = webpage_for_deep_crawling
        endpoint = "/publications/"
        url = baseurl + endpoint
        response = requests.get(url)
        plain_code = response.text
        html_code = BeautifulSoup(plain_code, "html.parser")
        author_name = html_code.find('h1').text
        result_container = html_code.findAll('li', {'class': re.compile('^list-result-item list-result-item.*')})
        same_as_before = ""
        # print(result_container)
        if len(result_container)==0:
            publication_info = [author_name, "N/A", "N/A", "N/A"]
            self.csv_writer.writerow(publication_info)
        for result in result_container:
            publication_year_div = result.find('div', {'class': 'search-result-group'})
            if publication_year_div is not None:
                publication_year = publication_year_div.text.strip()
                same_as_before = publication_year
            else:
                publication_year = same_as_before
            publication_link_attributes = result.find('a', {'class': 'link'})
            publication_link = publication_link_attributes.get('href')
            publication_name_span = publication_link_attributes.find('span')
            publication_name = publication_name_span.text
            publication_info=[author_name, publication_name, publication_link, publication_year]
            self.csv_writer.writerow(publication_info)
            print(author_name)
            print(publication_year)
            print(publication_link)
            print(publication_name)



WebCrawler()

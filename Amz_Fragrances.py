# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:24:58 2024

@author: sliu
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import pandas as pd
import time

vendor = pd.read_excel(r"C:/Users/sliu/Documents/File.xlsx")
vendor["UPC"] = vendor["Item UPC"]
vendor.dropna(subset=["UPC"], inplace=True)
vendor_list = vendor["UPC"].tolist()
newlist = []
for x in vendor_list:
    newlist.append(x.replace('-', ''))
#vendor_list = [int(x) for x in vendor_list]


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def initiate_driver(url = 'https://app.synccentric.com/products?from=single_keyword_search'):
    driver.get(url)
    
    username = driver.find_element("xpath", "//*[@type='email']")
    username.send_keys('email')
    password = driver.find_element("xpath", "//*[@type='password']")
    password.send_keys('password')
    login    = driver.find_element("xpath", "//*[@type='submit']")
    login.click()
    
    time.sleep(5)
    return driver
    
def filter_search(category = None):
    actions = ActionChains(driver)
    
    # Product Info filters
    driver.find_element("xpath", "//*[@name='Asin']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Brand']")).perform()
    driver.find_element("xpath", "//*[@name='Brand']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Category']")).perform()
    driver.find_element("xpath", "//*[@name='Category']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='EAN List']")).perform()
    driver.find_element("xpath", "//*[@name='EAN List']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Ean']")).perform()
    driver.find_element("xpath", "//*[@name='Ean']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Item Type Keyword']")).perform()
    driver.find_element("xpath", "//*[@name='Item Type Keyword']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Listing Url']")).perform()
    driver.find_element("xpath", "//*[@name='Listing Url']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Number of Items']")).perform()
    driver.find_element("xpath", "//*[@name='Number of Items']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Size']")).perform()
    driver.find_element("xpath", "//*[@name='Size']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Subcategory']")).perform()
    driver.find_element("xpath", "//*[@name='Subcategory']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Title']")).perform()
    driver.find_element("xpath", "//*[@name='Title']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='UPC List']")).perform()
    driver.find_element("xpath", "//*[@name='UPC List']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Upc']")).perform()
    driver.find_element("xpath", "//*[@name='Upc']").click()
    time.sleep(1)
    
    # Listing Info filters
    driver.find_element("xpath", "//*[@name='BB New Landed Price avg 1 mo']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='BB New Landed Price avg 12 mo']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='BB New Landed Price avg 3 mo']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='BB New Landed Price avg 6 mo']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Buy box seller']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Buybox New Landed Price']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Lowest New Price']")).perform()
    driver.find_element("xpath", "//*[@name='List Price Amount']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Lowest Offer Listings']")).perform()
    driver.find_element("xpath", "//*[@name='Lowest New Price']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Total Fees Estimate']")).perform()
    driver.find_element("xpath", "//*[@name='Reviews Total']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Sales Rank']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Sales Rank Category']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Sales Rank avg 1 month']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Sales Rank avg 12 months']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Sales Rank avg 3 months']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Sales Rank avg 6 months']").click()
    time.sleep(1)
    actions.move_to_element(driver.find_element("xpath", "//*[@name='Variable Closing Fee']")).perform()
    driver.find_element("xpath", "//*[@name='Second Lowest Landed Price']").click()
    time.sleep(1)
    driver.find_element("xpath", "//*[@name='Total New Sellers']").click()
    time.sleep(5)
    
    # Search the category
    driver.find_element("xpath", "//*[@value='category']").click()
    search = driver.find_element("xpath", "//*[@name='search-string']")
    search.send_keys(category)
    time.sleep(2)
    driver.find_element("xpath", "//*[@type='button']").click()  
    time.sleep(5)
    
def scrape_all():
    sheet = driver.page_source
    soup = BeautifulSoup(sheet, "html.parser")
    
    table = []
    for element in soup.select("tr")[51:]:
        table.append([td.get_text() for td in element.select("td")])
    return(table)
def scrape_upc(upc = None):
    # Search the upc
    driver.find_element("xpath", "//*[@value='identifier']").click()
    search = driver.find_element("xpath", "//*[@name='search-string']")
    search.send_keys(upc)
    time.sleep(2)
    driver.find_element("xpath", "//*[@type='button']").click()  
    time.sleep(8)
    
    sheet = driver.page_source
    soup = BeautifulSoup(sheet, "html.parser")
    
    table = []
    for element in soup.select("tr"):
        table.append([td.get_text() for td in element.select("td")])
    table = [item for item in table if len(item) == 31]
    if len(table) != 0:
        table[0].insert(0, "UPC")
        for i in range(1, len(table)):
            table[i].insert(0, upc)
            return(table)
   
######## UPC scrape
initiate_driver()
# filter_search()

items = []
for idx, upc in enumerate(newlist):
    if (idx+1) % 10 == 0:
        print(f"{idx+1} items searched")
    item_page = scrape_upc(upc)
    if item_page is not None:
        while item_page is not None:
            header = item_page[0]
            if header is not None:
                break
        items.extend(item_page[1:])           
    driver.refresh()
    time.sleep(5)
    
       
items_list = pd.DataFrame(items) 
items_list.columns = header
items_list.to_csv(r"C:/Users/sliu/Documents/File.csv", mode = 'a+', encoding='utf-8', index = False) 

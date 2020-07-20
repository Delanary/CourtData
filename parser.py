import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import pickle
import base64
import time


def get_link(link_num: int):
    return f"""https://bsr.sudrf.ru/bigs/portal.html#%7B%22start%22:{link_num * 10},%22rows%22:10,%22uid%22:%222e67c22d-855a-472b-80dd-b997bcb6438e%22,%22type%22:%22MULTIQUERY%22,%22multiqueryRequest%22:%7B%22queryRequests%22:%5B%7B%22type%22:%22Q%22,%22queryRequestRole%22:%22SIMPLE%22,%22request%22:%22%7B%5C%22query%5C%22:%5C%22%D0%9F%D1%80%D0%B8%D0%B7%D0%BD%D0%B0%D1%82%D1%8C%20%D0%B2%D0%B8%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9%5C%22,%5C%22type%5C%22:%5C%22QUERY%5C%22,%5C%22mode%5C%22:%5C%22SIMPLE%5C%22%7D%22,%22operator%22:%22AND%22%7D,%7B%22type%22:%22Q%22,%22request%22:%22%7B%5C%22mode%5C%22:%5C%22EXTENDED%5C%22,%5C%22typeRequests%5C%22:%5B%7B%5C%22fieldRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22case_user_doc_result_date%5C%22,%5C%22operator%5C%22:%5C%22B%5C%22,%5C%22query%5C%22:%5C%222019-01-01T00:00:00%5C%22,%5C%22sQuery%5C%22:%5C%222020-01-01T00:00:00%5C%22%7D,%7B%5C%22name%5C%22:%5C%22case_document_category_article_cat%5C%22,%5C%22operator%5C%22:%5C%22SEW%5C%22,%5C%22query%5C%22:%5C%22%D0%A1%D1%82%D0%B0%D1%82%D1%8C%D1%8F%20105%20%D0%A7%D0%B0%D1%81%D1%82%D1%8C%201%5C%22%7D,%7B%5C%22name%5C%22:%5C%22case_user_doc_result%5C%22,%5C%22operator%5C%22:%5C%22AW_CAL%5C%22,%5C%22query%5C%22:%5C%22%D0%92%D1%8B%D0%BD%D0%B5%D1%81%D0%B5%D0%BD%20%D0%9F%D0%A0%D0%98%D0%93%D0%9E%D0%92%D0%9E%D0%A0%5C%22,%5C%22sQuery%5C%22:null%7D%5D,%5C%22mode%5C%22:%5C%22AND%5C%22,%5C%22name%5C%22:%5C%22common%5C%22,%5C%22typesMode%5C%22:%5C%22AND%5C%22%7D%5D%7D%22,%22operator%22:%22AND%22,%22queryRequestRole%22:%22CATEGORIES%22%7D%5D%7D,%22sorts%22:%5B%7B%22field%22:%22score%22,%22order%22:%22desc%22%7D%5D,%22simpleSearchFieldsBundle%22:%22default%22,%22noOrpho%22:false,%22facet%22:%7B%22field%22:%5B%22type%22%5D%7D,%22facetLimit%22:21,%22additionalFields%22:%5B%22court_document_documentype1%22,%22court_case_entry_date%22,%22court_case_result_date%22,%22court_subject_rf%22,%22court_name_court%22,%22court_document_law_article%22,%22court_case_result%22,%22case_user_document_type%22,%22case_user_doc_entry_date%22,%22case_user_doc_result_date%22,%22case_doc_subject_rf%22,%22case_user_doc_court%22,%22case_doc_instance%22,%22case_document_category_article%22,%22case_user_doc_result%22,%22case_user_entry_date%22,%22m_case_user_type%22,%22m_case_user_sub_type%22,%22ora_main_law_article%22%5D,%22hlFragSize%22:1000,%22groupLimit%22:3,%22woBoost%22:false%7D"""


chromePath = '/home/delanary/Projects/NewGazeta/Selenium/chromedriver'


def get_links_by_search_link_id(link_id: int):
    url = get_link(link_id)
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chromePath, options=options)
    driver.get(url)
    for i in range(20):
        time.sleep(1)

        if "Уголовное дело" in driver.page_source:
            print("Got it")
            break
        print(f"Waited {i + 1} seconds ")
    lst = []
    for link in BeautifulSoup(driver.page_source, "lxml").find_all("a", href=True)[2:]:
        link = link["href"]
        if "javascript" not in link and link != "#":
            lst.append(link)
    return lst[1:]


lst = []
for i in range(163):
    lst += get_links_by_search_link_id(i)
    print(lst[:5])

with open("dumxuyp", "wb") as f:
    pickle.dump(lst, f)
f.close()

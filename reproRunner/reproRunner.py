from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from reproRunner import reproCommGenerator
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

import requests
import time
import os

browser = None
url = 'https://www.bp-london-ci.gmk.solutions.consensys-uk.net'

def reproAndCoverage(steps):
    # print('starting test')
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=options, executable_path=os.path.abspath("./chromedriver"))    
    login(browser)
    with open('./gremlins.min.js', 'r') as gremlins_js:
        gremlin = gremlins_js.read() 
        browser.execute_script(gremlin)
    for step in steps:
        com = reproCommGenerator.generateCommand(step)
        if com is not None:
            time.sleep(0.1) 
            browser.execute_script(com)
    # time.sleep(1) 
    temp_coverage = browser.execute_script("if (window.__coverage__) { return JSON.stringify(window.__coverage__)} else return 0")
    # print(temp_coverage)
    # coverage = 0
    
    response = requests.post('http://localhost:6969/coverage/client', headers={'Content-Type': 'application/json'}, data=temp_coverage)
    assert response.status_code == 200, "Failed to post coverage"
    coverageHtml = requests.get('http://localhost:6969/coverage').content
    soup = BeautifulSoup(coverageHtml, 'html.parser')
    coverage = soup.select('.fl.pad1y.space-right2:nth-child(2) > .strong')[0].text.replace('%', '')
    # time.sleep(500)
    browser.quit()
    print('coverage: ', float(coverage))
    return float(coverage)

def login(browser):
    browser.get(url)
    element1 = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    element2 = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    element3 = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "kc-login"))
    )
    element1.send_keys('superuser')
    element2.send_keys('z2L"Y!vYja>=')
    element3.click()
    element4 = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p[data-test-id='user-first-name']"))
    )
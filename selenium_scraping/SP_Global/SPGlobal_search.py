import time
import httpx
import json
import lxml.html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ALLOWED_DOMAINS = ("https://www.spglobal.com",)
REQUEST_DELAY = 0.1



def make_request(url):
    """
    ***TAKEN FROM PA3 CODE SUPPLIED BY INSTRUCTOR***
    Make a request to `url` and return the raw response.

    This function ensure that the domain matches what is expected
    and that the rate limit is obeyed.
    """
    # check if URL starts with an allowed domain name
    for domain in ALLOWED_DOMAINS:
        if url.startswith(domain):
            break
    else:
        # note: this else is indented correctly, it is a less-commonly used
        # for-else statement.  the condition is only met if the for loop
        # *never* breaks, i.e. no domains match
        raise ValueError(f"can not fetch {url}, must be in {ALLOWED_DOMAINS}")
    time.sleep(REQUEST_DELAY)
    print(f"Fetching {url}")
    resp = httpx.get(url)
    resp.raise_for_status()
    return resp
    
def company_name(ticker):
    
    with open("SA_sp500_tickers.json", "r") as file:
        data = json.load(file)

        return data[ticker]['company_name']
    
def search_esg_spglobal(ticker):

    base_url = "https://www.spglobal.com/esg/scores/results?"
    #response = make_request(base_url)
    
    company = company_name(ticker)
    
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  
    chrome_options.add_argument("--user-data-dir=/tmp/chrome_data")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(base_url)
    time.sleep(5)

    try:
        print("Start scraping...")
        search_bar = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.banner-search__input"))
        )
        print("Found search bar...")

        search_bar.send_keys(company)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(5)

        ticker_page_url = driver.current_url
        print("ticker page url:", ticker_page_url)

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

make_request('https://www.spglobal.com/esg/scores/results?')
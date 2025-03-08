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

ALLOWED_DOMAINS = ("https://www.msci.com/",)
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
     
def search_msci_ESG(ticker):

    base_url = "https://www.msci.com/our-solutions/esg-investing/esg-fund-ratings-climate-search-tool"
    #response = make_request(base_url)
       
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome_data")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(base_url)
    time.sleep(5)

    try:
        print("Start scraping...")
        #Having trouble with inputting data in the search bar, might be related to a Shadow DOM
        #due to HTML tag that says "Shadow Content (user agent)". 
        #shadow_host = driver.find_element(By.CSS_SELECTOR, "input.msci-ac-search-input")
        #shadow_root = driver.execute_script("returnarguments[0].shadowRoot", shadow_host)
        
        search_bar = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.msci-ac-search-input"))
        )
        print("Found search bar...")

        search_bar.send_keys(ticker)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(5)

        try:
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "header-esg-industry"))
            )

            print("Search results loaded")
            print("Industry", result.text)
            
            #ticker_page_url = driver.current_url
            #print("ticker page url:", ticker_page_url)

        except Exception:
            print("No search results")

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

#make_request('https://www.msci.com/our-solutions/esg-investing/esg-fund-ratings-climate-search-tool')
search_msci_ESG('AAPL')
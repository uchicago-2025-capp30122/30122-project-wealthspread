import time
import httpx
import json
import lxml.html

ALLOWED_DOMAINS = ("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",)
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
    
def scrape_sp500_page(url):
    """
    This function takes a URL to Wikipedia's S&P500 page and returns a
    nested dictionary with the unique symbol (ticker), external url to the stock's exchange page, 
    security name, and a url to the security's wikipedia page.

    Parameters:
        * url:  a URL to a wikipedia page with a list of the S&P500 securities

    Returns:
        A nested dictionary with the following keys:
            * symbol:           stock symbol (ticker) of the security
            * exchange_url:     link to the security's page on the exchange
            * security:         the name of the security
            * wiki_page:        link to the wikipedia page of the security
    """
    resp = make_request(url)
    root = lxml.html.fromstring(resp.text)

    symbol_path = '//table[contains(@class, "wikitable")]//tr/td[1]/a[@class="external text"]'
    symbols = root.xpath(f"{symbol_path}/text()")
    symbol_urls = root.xpath(f"{symbol_path}/@href")

    security_path = '//table[contains(@class, "wikitable")]//tr/td[2]/a'
    securities = root.xpath(f"{security_path}/text()")
    securities_wiki = root.xpath(f"{security_path}/@href")

    sp500_dict = {}

    for symbol, link, security, wiki in zip(symbols, symbol_urls, securities, securities_wiki):
        sp500_dict[symbol] = {"exchange_url": link, 
                              "security": security, 
                              "wiki_page": "https://en.wikipedia.org" + wiki}

    print(f"Scraped {len(sp500_dict)} tickers")
    #assert len(sp500_dict) == 500, f"Expected 500 tickers, but received {len(sp500_dict)}"
    #turns out there's > 500 stocks in the S&P500, big fail

    filename = "Wiki_sp500_tickers.json"
    with open(filename, "w") as file:
        json.dump(sp500_dict, file, indent=2)

    print(f"Saved {len(sp500_dict)} tickers to {filename}")

scrape_sp500_page("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
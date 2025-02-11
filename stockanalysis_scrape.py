import time
import httpx
import json
import lxml.html

ALLOWED_DOMAINS = ("https://stockanalysis.com/list/sp-500-stocks/",)
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
            * ticker:         stock symbol (ticker) of the security
            * name:           the name of the security
            * webpage:        link to the wikipedia page of the security
    """
    sp500_dict = {}
    
    resp = make_request(url)
    root = lxml.html.fromstring(resp.text)

    rows = root.xpath("//table[@id='main-table']//tr")

    for row in rows[1:]:
        ticker_col = row.xpath("./td[2]/a")
        ticker = ticker_col[0].text.strip()
        
        sp500_dict[ticker] = {
            "webpage": "https://stockanalysis.com" + ticker_col[0].get('href').strip(),
            "company_name": row.xpath("./td[3]/text()")[0].strip(),
            "market_cap": row.xpath("./td[4]/text()")[0].strip(),
            "stock_price": row.xpath("./td[5]/text()")[0].strip(),
            "pct_change": row.xpath("./td[6]/text()")[0].strip(),
            "revenue": row.xpath("./td[7]/text()")[0].strip()}

    print(f"Scraped {len(sp500_dict)} tickers")

    filename = "SA_sp500_tickers.json"
    with open(filename, "w") as file:
        json.dump(sp500_dict, file, indent=2)

    print(f"Saved {len(sp500_dict)} tickers to {filename}")

scrape_sp500_page("https://stockanalysis.com/list/sp-500-stocks/")
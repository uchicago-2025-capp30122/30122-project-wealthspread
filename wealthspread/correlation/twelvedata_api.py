ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz1234567890%+,^=._"
import requests
import csv
import json
from io import StringIO
from pathlib import Path
import os
import time

def tickers_list_creator():
    tickers_list = []
    tickers_file = "SA_sp500_tickers.json"
    with open(tickers_file,"r") as ticker_file:
        tickers = json.load(ticker_file)
        for key, val in tickers.items():
            tickers_list.append(key)
    print(f"Length is {len(tickers_list)}")
    return tickers_list
    
    
def calculate_weight_of_portfolio(current_stocks_investment_amounts):
    """
    Calculate the weight of each stock in the portfolio based on investment amounts.

    Parameters:
    current_stocks_investment_amounts (dict): A dictionary where keys are stock tickers (str) 
                                              and values are investment amounts (float or int).

    Returns:
    dict: A dictionary where keys are stock tickers and values are their respective weights 
          in the portfolio, summing to 1.
    """
    total_investment = sum(current_stocks_investment_amounts.values())
    weights = {}
    
    for ticker, amount in current_stocks_investment_amounts.items():
        weights[ticker] = amount / total_investment
    
    return weights 


CACHE_DIR = Path(__file__).parent / "_cache2"
# Cache dictionary to store all API responses for multiple tickers
cache = {}


def url_to_cache_key(url: str) -> str:
    """
    Convert a URL to a cache key that can be stored on disk.

    The rules are as follows:

    1) All keys should be lower case. URLs are case-insensitive.
    2) The leading http(s):// should be removed.
    3) The remaining characters should all be in ALLOWED_CHARS.
       Any other characters should be converted to `_`.

    This lets us have unique filenames that are safe to write to disk.
    Some characters (notably `/`) would cause problems if not removed.
    """

    lowered = url.lower()
    removed_lowered = lowered.lstrip("http(s)://")
    updated_url = ""
    for charac in removed_lowered:
        if charac not in ALLOWED_CHARS:
            updated_url += "_"
        else:
            updated_url += charac        
    return updated_url

def fetch_and_cache(tickers=None):
    if tickers == None:
        tickers = tickers_list_creator()
        CACHE_DIR.mkdir(exist_ok=True)
        cache = {} 
        for ticker in tickers: 
            time.sleep(10)
            updated_url = url_to_cache_key(f"https://api.twelvedata.com/time_series?apikey=330256b3d0894fec82b468d4d763bd04&interval=1day&symbol={ticker}&start_date=2020-02-01 02:01:00&end_date=2025-02-01 02:01:00&format=CSV")
            new_path = os.path.join(CACHE_DIR, updated_url)
            #new_path = CACHE_DIR / f"{updated_url}.json"

            
            if os.path.exists(new_path):
                with Path(new_path).open("r") as f:
                    content = f.read()
                    print(f"Data for {ticker} was already fetched and cached previously")
                    data_dict = parse_csv_to_dict(content)
                    cache[ticker] = data_dict  # Save the parsed dictionary in cache
                    

                #   return cache
    
            else:
                response = requests.get(f"https://api.twelvedata.com/time_series?apikey=330256b3d0894fec82b468d4d763bd04&interval=1day&symbol={ticker}&start_date=2020-02-01 02:01:00&end_date=2025-02-01 02:01:00&format=CSV")
                if response.status_code == 200:
                    response_text = response.text
                    with Path(new_path).open("w") as f:
                        f.write(response_text)
                        print('Fetching')

                        data_dict = parse_csv_to_dict(response_text)
                        cache[ticker] = data_dict  # Save the parsed dictionary in cache
                       
                        print(f"Data for {ticker} fetched and cached now.")
                        
        with open("company_info.json", "w") as output_file:
            json.dump(cache, output_file, indent=4)           
        
        # print(cache)
        # for key, value in cache.items(): 
        #     print(key)
    


def parse_csv_to_dict(csv_data):
    # Use StringIO to treat the string as a file for the csv.reader
    f = StringIO(csv_data)
    reader = csv.DictReader(f, delimiter=";")
    
    # Create a dictionary where dates are the keys and only the close price is saved
    data_dict = {}
    for row in reader:
        date = row["datetime"]
        close_price = row["close"]
        data_dict[date] = close_price
    
    print(f"Parsed dictionary: {data_dict}")  # Debug print to check the parsed data
    return data_dict

def count_companies():

    with open('company_info.json', 'r') as f: 
        contents = json.load(f)
        print(len(contents))
            




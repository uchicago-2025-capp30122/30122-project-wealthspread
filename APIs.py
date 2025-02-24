import json
import requests
import pandas as pd
import time
import logging
import os
from tqdm import tqdm

# Constants
API_KEY = "c8e34b970f504014b1bdfa7f289d8ea5"

class TwelveDataAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.twelvedata.com"
        self.session = requests.Session()
        self.last_call_time = time.time()
        
        # Get absolute path for cache directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.cache_dir = os.path.join(current_dir, "stock_json_cache")
        
        # Create cache directory
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            print(f"Created cache directory at: {self.cache_dir}")
        else:
            print(f"Using existing cache directory at: {self.cache_dir}")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='stock_data_fetch.log'
        )
        self.logger = logging.getLogger(__name__)

    def _get_cache_path(self, symbol):
        """Get absolute cache file path"""
        return os.path.join(self.cache_dir, f"{symbol}.json")

    def _get_from_cache(self, symbol):
        """Try to get data from cache"""
        cache_path = self._get_cache_path(symbol)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    print(f"Retrieved {symbol} from cache: {cache_path}")
                    return data
            except Exception as e:
                self.logger.error(f"Error reading cache for {symbol} at {cache_path}: {e}")
        return None

    def _save_to_cache(self, symbol, data):
        """Save API response to cache"""
        cache_path = self._get_cache_path(symbol)
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {symbol} to cache: {cache_path}")
        except Exception as e:
            self.logger.error(f"Error saving cache for {symbol} at {cache_path}: {e}")

    def _rate_limit_handler(self):
        elapsed = time.time() - self.last_call_time
        if elapsed < 25:  # 13 seconds between calls
            time.sleep(5 - elapsed)
        self.last_call_time = time.time()

    def get_stock_data(self, symbol, start_date, end_date):
        """Get stock data with caching"""
        # Try to get from cache first
        cached_data = self._get_from_cache(symbol)
        if cached_data is not None:
            return cached_data

        # If not in cache, fetch from API
        self._rate_limit_handler()
        print(f"Fetching {symbol} from API...")
        
        endpoint = f"{self.base_url}/time_series"
        params = {
            "symbol": symbol,
            "interval": "1day",
            "apikey": self.api_key,
            "start_date": start_date,
            "end_date": end_date,
            "format": "JSON"
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save to cache if request was successful
            if 'values' in data:
                self._save_to_cache(symbol, data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching data for {symbol}: {e}")
            return None

def main():
    try:
        # Load the S&P 500 data
        with open('Wiki_sp500_tickers.json', 'r') as f:
            sp500_data = json.load(f)
        
        # Initialize API client
        api_client = TwelveDataAPI()
        
        # Process each company
        print("\nFetching stock data for each company...")
        for symbol, info in tqdm(sp500_data.items(), desc="Processing companies"):
            data = api_client.get_stock_data(
                symbol=symbol,
                start_date="2020-01-01 16:51:00",
                end_date="2025-02-22 16:52:00"
            )
            
            if data and 'values' in data:
                print(f"Successfully processed {symbol}")
            else:
                print(f"No data received for {symbol}")
        
        print("\nProcess completed!")
        print(f"- JSON responses are cached in: {api_client.cache_dir}")
        print("- Check 'stock_data_fetch.log' for detailed processing information")
        
        # Verify cache contents
        cached_files = os.listdir(api_client.cache_dir)
        print(f"\nTotal files in cache: {len(cached_files)}")
        print("Sample of cached files:")
        for file in sorted(cached_files)[:5]:
            print(f"- {file}")
        
    except FileNotFoundError:
        print("Error: Wiki_sp500_tickers.json not found. Please ensure the file exists in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Process failed: {e}")

if __name__ == "__main__":
    main()
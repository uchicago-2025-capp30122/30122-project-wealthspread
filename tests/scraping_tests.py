import pytest
import json
from pathlib import Path

path = Path(__file__).parent /"../wealthspread/scrape/"

def test_count_tickers():
    file_path = path / "SA_sp500_tickers.json"
    with file_path.open('r') as file:
        data = json.load(file)
    
    assert len(data) >= 500, f"Expected at least 500 tickers, received {len(data)}"

def test_ticker_length():
    file_path = path / "SA_sp500_tickers.json"
    with file_path.open('r') as file:
        data = json.load(file)

    for ticker in data.keys():
        assert 1 <= len(ticker) <= 5, f"Ticker {ticker} has an invalid length: {len(ticker)}"

def test_check_ticker_webpages():
    file_path = path / "SA_sp500_tickers.json"
    with file_path.open('r') as file:
        data = json.load(file)
    
    for ticker, info in data.items():
        webpage = info.get('webpage')
        assert webpage, f"Webpage for {ticker} is missing, didn't scrape correctly"
        assert webpage.strip(), f"Webpage for {ticker} is empty, didn't scrape correctly"

def test_count_companies():
    file_path = path / "company_info.json"
    with file_path.open('r') as file:
        data = json.load(file)
    
    assert len(data) >= 500, f"Expected at least 500 companies, received {len(data)}"

def test_company_info():
    file_path = path / "company_info.json"
    with file_path.open('r') as file:
        data = json.load(file)
    
    for ticker, info in data.items():
        assert len(info) > 0, f"Company information for {ticker} is missing."

import pytest
import json

def test_count_tickers():
    with open('../wealthspread/scrape/SA_sp500_tickers.json', 'r') as file:
        data = json.load(file)
    
    assert len(data) == 503, f"Expected 503 tickers, received {len(data)}"

def test_check_ticker_webpages():
    with open('../wealthspread/scrape/SA_sp500_tickers.json', 'r') as file:
        data = json.load(file)
    
    for ticker, info in data.items():
        webpage = info.get('webpage')
        assert webpage, f"Webpage for {ticker} is missing, didn't scrape correctly"
        assert webpage.strip(), f"Webpage for {ticker} is empty, didn't scrape correctly"

def test_count_companies():
    with open('../wealthspread/scrape/company_info.json', 'r') as file:
        data = json.load(file)
    
    assert len(data) == 503, f"Expected 503 companies, received {len(data)}"

def test_company_info():
    with open('../wealthspread/scrape/company_info.json', 'r') as file:
        data = json.load(file)
    
    for ticker, info in data.items():
        assert len(info) > 0, f"Company information for {ticker} is missing."

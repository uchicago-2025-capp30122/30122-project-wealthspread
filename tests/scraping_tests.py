import pytest
import json

def test_ticker_count():
    with open('../wealthspread/scrape/SA_sp500_tickers.json', 'r') as file:
        data = json.load(file)
    assert len(data) == 503, f"Expected 503 tickers, received {len(data)}"

def test_company_count():
    with open('../wealthspread/scrape/company_info.json', 'r') as file:
        data = json.load(file)
    assert len(data) == 503, f"Expected 503 companies, received {len(data)}"

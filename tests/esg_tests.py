import pytest
import json

def test_count_esg():
    with open('../wealthspread/esg/ESG_Scores.json', 'r') as file:
        data = json.load(file)
    
    assert len(data) == 503, f"Expected 503 tickers, received {len(data)}"

def test_missing_esg():
    with open('../wealthspread/esg/ESG_Scores.json', 'r') as file:
        data = json.load(file)

    for ticker, esg in data.items():
        if isinstance(esg, dict):
            required_scores = ['totalEsg',
                             'environmentScore',
                             'socialScore',
                             'governanceScore']
            for score in required_scores:
                assert score in esg, f"Missing {score} for {ticker}"
        
        elif "No ESG data available" in esg:
            continue
        
        else:
            pytest.fail(f"Expected ESG data or alternate message for {ticker}.")
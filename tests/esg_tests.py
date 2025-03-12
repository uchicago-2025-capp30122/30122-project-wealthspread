import pytest
import json
from pathlib import Path

path = Path(__file__).parent /"../wealthspread/esg/"

def test_count_esg():
    file_path = path / "ESG_Scores.json"
    with file_path.open('r') as file:
        data = json.load(file)
    
    assert len(data) >= 500, f"Expected at least 500 tickers, received {len(data)}"

def test_missing_esg():
    file_path = path / "ESG_Scores.json"
    with file_path.open('r') as file:
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

def test_total_esg_sum():
    file_path = path / "ESG_Scores.json"
    with file_path.open('r') as file:
        data = json.load(file)

        for ticker, esg in data.items():
            if isinstance(esg, dict):
                total_esg = esg.get("totalEsg")
                env_score = esg.get("environmentScore")
                social_score = esg.get("socialScore")
                gov_score = esg.get("governanceScore")

                if None not in {total_esg, env_score, social_score, gov_score}:
                    assert total_esg == pytest.approx(env_score + social_score + gov_score, abs=0.05), \
                        f"ESG sum mismatch for {ticker}: {env_score} + {social_score} + {gov_score} != {total_esg}"
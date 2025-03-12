import yfinance as yf # This is the Yahoo Finance API library (regular web-API unavailable to general public)
from requests.exceptions import RequestException
import pandas as pd
import json

def esg_scores(ticker):
    '''
    Function takes a ticker (stock symbol) and returns ESG Risk Score
    sourced from the yfinance (Yahoo Finance) API / Python library.
    Yahoo Finance employs ESG risk scores from Sustainalytics (a 
    Morningstar company).
    '''
    # yfinance method to get specific ticker data
    stock = yf.Ticker(ticker)
    try:
        # yfinance method to get ESG data
        esg_data = stock.sustainability
        if esg_data is None or esg_data.empty:
            return None
        else:
            # yfinance returns results in dataframe format
            esg_df = pd.DataFrame(esg_data)

            # pull only these specific sustainability metrics
            scores = esg_df.index.intersection([
                'totalEsg',
                'environmentScore',
                'socialScore',
                'governanceScore'])

            if len(scores) == 0:
                return None
            
            filtered_df = esg_df.loc[scores]
            return filtered_df.to_dict()['esgScores']
    
    except RequestException as e:
        return f"No ESG Data for {ticker}"
    except Exception as e:
        return f"No ESG Data for {ticker}"

# Grab unique tickers from the S&P500
with open('../scrape/SA_sp500_tickers.json', 'r') as file:
    data = json.load(file)

# Load S&P500 yfinance ESG results into dictionary, then dump to json
esg_dict = {}
for ticker, info in data.items():
    result = esg_scores(ticker)
    if result:
        esg_dict[ticker] = result
    else:
        esg_dict[ticker] = f"No ESG data available for {ticker}."
with open("ESG_Scores.json", "w") as file:
    json.dump(esg_dict, file, indent=2)
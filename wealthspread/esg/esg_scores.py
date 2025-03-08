import yfinance as yf
import requests
from requests.exceptions import RequestException
import pandas as pd
import json

def esg_scores(ticker):
    stock = yf.Ticker(ticker)
    
    try:
        esg_data = stock.sustainability
        if esg_data is None or esg_data.empty:
            return None
        else:
            esg_df = pd.DataFrame(esg_data)
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
        #print(f"404 Error for {ticker}: {e}")
        return f"No ESG Data for {ticker}"
    except Exception as e:
        #print(f"Exception for {ticker}: {e}")
        return f"No ESG Data for {ticker}"

    

with open('../SA_sp500_tickers.json', 'r') as file:
    data = json.load(file)

esg_dict = {}
for ticker, info in data.items():
    result = esg_scores(ticker)
    if result:
        esg_dict[ticker] = result

with open("ESG_Scores.json", "w") as file:
    json.dump(esg_dict, file, indent=2)

print(len(esg_dict))

#print(esg_scores('AAPL'))
import numpy as np
import pandas as pd
import json
from itertools import combinations
from twelvedata_api import tickers_list_creator

ALL_STOCKS = tickers_list_creator()

def convert_to_percentchange():
    with open("company_info.json", "r") as file:
        content = json.load(file)
    percent_changes = {}
    for ticker, prices in content.items():
        changes = {}
        curr_date, curr_price = None, None
        for prev_date, prev_price in prices.items():
            if curr_date is not None:
                change = ((float(curr_price) - float(prev_price)) / float(prev_price)) * 100
                changes[curr_date] = round(change, 4)
            curr_date, curr_price = prev_date, prev_price
        percent_changes[ticker] = changes
        print(f"Just did {ticker}")

    with open("percent_changes.json", "w") as file:
        json.dump(percent_changes, file, indent=4) 

    return percent_changes


        
# Function to compute weighted mean correlation
def weighted_mean_correlation(corr_matrix, weights):
    weights_array = np.array(list(weights.values()))
    weighted_corr = corr_matrix * np.outer(weights_array, weights_array)
    mean_corr = weighted_corr.sum() / weights_array.sum()
    total_mean_corr = mean_corr.mean() 
    return total_mean_corr


def correlation_matrix():
    with open('percent_changes.json', 'r') as file:
        contents = json.load(file)
    df = pd.DataFrame(contents)

    # Compute correlation matrix
    corr_matrix = df.corr()
    corr_matrix.to_csv("correlation_matrix.csv", index=True)


def suggest_stocks(current_inv, investment_amount):
    """
    current_inv: dict {ticker: amount_invested}
    investment_amount: float (new money to be invested)
    ALL_STOCKS: list of tickers to consider adding
    """
    current_tickers = list(current_inv.keys())
    current_amounts = np.array(list(current_inv.values()))
    corr_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)
    # Determine how many stocks to suggest
    if len(current_tickers) == 1:
        possible_additions = list(combinations(ALL_STOCKS, 2))
    else:
        possible_additions = [stock for stock in ALL_STOCKS if stock not in current_inv]
    best_combination = None
    best_correlation = float("inf")

    for new_stocks in possible_additions:
        new_tickers = current_tickers + [new_stocks]
    
        # Compute new weights
        new_amounts = np.append(current_amounts, investment_amount)
        new_weights = {ticker: float(amt / new_amounts.sum())for ticker, amt in zip(new_tickers, new_amounts)}

        # Extract sub-matrix
        sub_corr_matrix = corr_matrix.loc[new_tickers, new_tickers]

        # Compute weighted mean correlation
        total_mean_corr = weighted_mean_correlation(sub_corr_matrix, new_weights)

        # Find the best combination that minimizes correlation
        if abs(total_mean_corr) < abs(best_correlation):
            best_correlation = total_mean_corr
            best_combination = new_stocks


    return f"We suggest investing in {best_combination}, Portfolio correlation would be {float(np.round(best_correlation,3))}"




# Example Usage
#simulation.suggest_stocks({"CTAS":10000, "BKR":20000, "ORCL":15000}, 10000)
# simulation.suggest_stocks({"CTAS":10000, "BKR":20000, "AMZN":15000, "PM": 5000}, 10000)
# simulation.suggest_stocks({"DIS":1000, "CTAS":1000, "ISRG":1000, "BKR" :1000, "MRNA": 1000}, 1000)
# simulation.suggest_stocks({"MS":1000, "CTAS":1000, "AXP":1000, "BKR" :1000, "MRNA": 1000}, 1000)
# simulation.suggest_stocks({"TMUS":1000, "CTAS":1000, "MCD":1000, "BKR" :1000, "MRNA": 1000}, 1000)

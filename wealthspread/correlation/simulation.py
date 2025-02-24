import numpy as np
import pandas as pd
import json
from itertools import combinations
from correlation import tickers_list_creator

ALL_STOCKS = tickers_list_creator()

def calculate_weight_of_portfolio(current_inv = {'GOOG': 10000, 'AAPL' : 20000,
                                                 'MSFT' : 20000}):
    """
    Calculate the weight of each stock in the portfolio based on investment amounts.

    Parameters:
    current_inv (dict): A dictionary where keys are stock tickers (str) 
                                              and values are investment amounts (float or int).

    Returns:
    dict: A dictionary where keys are stock tickers and values are their respective weights 
          in the portfolio, summing to 1.
    """
    total_investment = sum(current_inv.values())
    weights = {}
    
    for ticker, amount in current_inv.items():
        weights[ticker] = amount / total_investment
    
    return weights

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
    print('weight arrary', weights_array)
    
    weighted_corr = corr_matrix * np.outer(weights_array, weights_array)  # Apply weights
    print(np.outer(weights_array, weights_array), 'npouter')
    print(weighted_corr, 'weight corr')
    
    mean_corr = weighted_corr.sum() / weights_array.sum()
    print(mean_corr , 'meancorr')
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
    # print(current_tickers)
    # print(current_amounts)
    corr_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)
    # print(corr_matrix)
    # Determine how many stocks to suggest
    if len(current_tickers) == 1:
        num_suggestions = 2
        possible_additions = list(combinations(ALL_STOCKS, 2))
        # print(possible_additions,"if")
    else:
        num_suggestions = 1
        # possible_additions = [(stock) for stock in ALL_STOCKS]  #we removed the comma 
        possible_additions = [stock for stock in ALL_STOCKS if stock not in current_inv]

       # print(possible_additions,"else")
    best_combination = None
    best_correlation = float("inf")

    for new_stocks in possible_additions:
        print(new_stocks, 'new stocks') 
        new_tickers = current_tickers + [new_stocks] #[stock for stock in new_stocks if stock not in current_tickers]
        print(new_tickers, 'new_ticker')
        print(new_stocks, 'new_stock') 
        print(current_tickers, 'curr')
    
        # Compute new weights
        new_amounts = np.append(current_amounts, investment_amount) #[investment_amount / len(new_stocks)] * len(new_stocks))
        print(new_amounts, 'new amount')
        new_weights = {ticker: float(amt / new_amounts.sum() )for ticker, amt in zip(new_tickers, new_amounts)}
        print(new_weights)

        # Extract sub-matrix
        sub_corr_matrix = corr_matrix.loc[new_tickers, new_tickers]
        print(sub_corr_matrix , 'submatrix') 
        # Compute weighted mean correlation
        total_mean_corr = weighted_mean_correlation(sub_corr_matrix, new_weights)
        print(total_mean_corr, 'total_ mean corr') 
        # Find the best combination that minimizes correlation
        if abs(total_mean_corr) < abs(best_correlation):
            best_correlation = total_mean_corr
            best_combination = new_stocks

    return best_combination, float(best_correlation) 

# Example Usage
# current_inv = {"GOOG": 10000, "AAPL": 20000, "MSFT": 20000}  # Current portfolio
# investment_amount = 10000  # New investment amount

# best_stocks, correlation = suggest_stocks(current_inv, investment_amount)
# print(f"Suggested Stocks: {best_stocks}, New Mean Correlation: {correlation:.4f}")
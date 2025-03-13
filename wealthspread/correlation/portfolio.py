import numpy as np
import pandas as pd
import json
from itertools import combinations
from wealthspread.correlation.simulation import weighted_mean_correlation
from wealthspread.correlation.twelvedata_api import tickers_list_creator
# from twelvedata_api import tickers_list_creator
# from simulation import weighted_mean_correlation
# to run the suggest_stocks_sharpe independently(i.e not from CLI) change path by
# unhashing above 2 paths and hashing the paths above them.

ALL_STOCKS = tickers_list_creator()

def scale_returns():
    "Scales the returns of stocks with very high historical returns"

    # Load the dictionary from the JSON file
    input_file = "geometric_mean.json"
    output_file = "scaled_geometric_mean.json"

    with open(input_file, "r") as file:
        stock_returns = json.load(file)

    # Apply the cap of 0.45 on stock returns
    capped_stock_returns = {stock: min(return_value, 0.45) for stock, return_value in stock_returns.items()}

    # Save the modified dictionary to a new JSON file
    with open(output_file, "w") as file:
        json.dump(capped_stock_returns, file, indent=4)

    # Confirm completion
    output_file

def all_geometric_mean():
    "Creates a file with the geometric means of all the stocks"
    
    all_geo_means = {}
    with open('stock_prices.json', 'r') as file:
        stocks_data = json.load(file)
        for ticker in stocks_data.keys():
            data = stocks_data[ticker]
            dates = list(data.keys())
            start_date = dates[-1]  # First date in the data (earliest)
            end_date = dates[0]    # Last date in the data (most recent)
        
            start_price = float(data[start_date])
            end_price = float(data[end_date])
            
        # Calculate geometric mean using the formula
            geometric_mean = (end_price / start_price) ** (1 / 5) - 1
            all_geo_means[ticker] = geometric_mean

   # Save dictionary to a JSON file
    with open("geometric_mean.json", "w") as file:
        json.dump(all_geo_means, file, indent=4)

def portfolio_geometric_mean(data, new_weights): 
    "Returns the portfolios geometric mean by taking each stocks return and weights"
    
    lst = []     
    for ticker, weight in new_weights.items():
        ret = data[ticker]
        weighted_geometric_mean = ret * weight
        lst.append(weighted_geometric_mean)
    
    return sum(lst) 


def suggest_stocks_sharpe(current_inv, investment_amount):
    """
    Main function that returns the stock with the highest sharpe ratio
    Inputs: current_inv: dict {ticker: amount_invested}, 
    investment_amount: float (new money to be invested)
    Output: A list [Suggested Stock, Sharpe Ratio, Portfolio Correlation, 
    Old Portfolio ESG, New Portfolio ESG]
    """
    current_tickers = list(current_inv.keys())
    current_amounts = np.array(list(current_inv.values()))
    corr_matrix = pd.read_csv("wealthspread/correlation/correlation_matrix.csv", index_col=0)
    
    with open("wealthspread/correlation/scaled_geometric_mean.json", "r") as file:
        geo_means_dict = json.load(file)
    
    with open("wealthspread/correlation/ESG_Scores.json", "r") as file:  
        esg_scores = json.load(file) 

    # Determine how many stocks to suggest
    if len(current_tickers) == 1:
        possible_additions = list(combinations(ALL_STOCKS, 2))
    else:
        possible_additions = [stock for stock in ALL_STOCKS if stock not in current_inv]
    best_combination = None
    # best_correlation = float("inf")
    best_sharpe = 0

    for new_stocks in possible_additions: 
        new_tickers = current_tickers + [new_stocks]
        # Compute new weights
        new_amounts = np.append(current_amounts, investment_amount)
        new_weights = {ticker: float(amt / new_amounts.sum())for ticker, amt in zip(new_tickers, new_amounts)}
      
        # Extract sub-matrix
        sub_corr_matrix = corr_matrix.loc[new_tickers, new_tickers]
      
        # Compute weighted mean correlation 
        total_mean_corr = weighted_mean_correlation(sub_corr_matrix, new_weights)
        
        total_mean_return = portfolio_geometric_mean(geo_means_dict, new_weights)
        # Find the best combination that minimizes correlation
        sharpe_ratio = total_mean_return / total_mean_corr 
        
        if abs(sharpe_ratio) > abs(best_sharpe):
            best_sharpe = sharpe_ratio
            best_combination = new_stocks

    new_stock = best_combination[0] if isinstance(best_combination, tuple) else best_combination

    # Compute weighted ESG score for the current portfolio
    current_esg_score = sum(
        current_inv[ticker] * esg_scores.get(ticker, {}).get("totalEsg", 0)  
        for ticker in current_tickers
    ) / sum(current_inv.values()) if current_inv else 0

    # Compute weighted ESG score for the new portfolio
    new_portfolio_inv = {**current_inv, new_stock: investment_amount} 
    new_esg_score = sum(
        new_portfolio_inv[ticker] * esg_scores.get(ticker, {}).get("totalEsg", 0) 
        for ticker in new_portfolio_inv
    ) / sum(new_portfolio_inv.values()) if new_portfolio_inv else 0

    return [best_combination, float(np.round(best_sharpe,3)), float(np.round(total_mean_corr,3)), np.round(current_esg_score,2), np.round(new_esg_score,2)]

    # Example Usage:
    # portfolio.suggest_stocks_sharpe({"FI":1000, "BA":1000, "USB":1000, "CMG" :1000, "TDG": 1000}, 1000)
    # portfolio.suggest_stocks_sharpe({"BK":1000, "GM":1000, "D":1000, "LULU" :1000, "MPC": 1000}, 1000)
    # portfolio.suggest_stocks_sharpe({"PLD":1000, "COP":1000, "ETN":1000, "LOW" :1000, "HON": 1000}, 1000)
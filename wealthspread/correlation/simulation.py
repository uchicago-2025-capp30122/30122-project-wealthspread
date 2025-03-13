import numpy as np
import pandas as pd
import json
from itertools import combinations
from .twelvedata_api import tickers_list_creator

ALL_STOCKS = tickers_list_creator()

def convert_to_percentchange():
    "Converts the returns into daily percent change so that it can be used "
    "to calculate correlations"

    with open("company_info.json", "r") as file:
        content = json.load(file)
    percent_changes = {}
    # Iterate over each stock
    for ticker, prices in content.items():
        changes = {}
        curr_date, curr_price = None, None

        # Iterate over each curr dat and prev day
        for prev_date, prev_price in prices.items():
            if curr_date is not None:
                change = ((float(curr_price) - float(prev_price)) / float(prev_price)) * 100
                changes[curr_date] = round(change, 4)
            curr_date, curr_price = prev_date, prev_price
        percent_changes[ticker] = changes

    # Create a json file
    with open("percent_changes.json", "w") as file:
        json.dump(percent_changes, file, indent=4) 

    return percent_changes
   

def weighted_mean_correlation(corr_matrix, weights):
    "Function to compute weighted mean correlation"

    weights_array = np.array(list(weights.values()))
    weighted_corr = corr_matrix * np.outer(weights_array, weights_array)
    mean_corr = weighted_corr.sum() / weights_array.sum()
    total_mean_corr = mean_corr.mean() 
    return total_mean_corr


def correlation_matrix():
    "Uses the percent changes to create a correlation matrix of all stocks "
    "with each other"
    with open('percent_changes.json', 'r') as file:
        contents = json.load(file)
    df = pd.DataFrame(contents)

    # Compute correlation matrix
    corr_matrix = df.corr()
    corr_matrix.to_csv("correlation_matrix.csv", index=True)
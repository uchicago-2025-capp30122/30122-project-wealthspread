# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import json
from itertools import combinations
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your Canva website

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load data files (ensure these are in the same directory as your API)
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Function adapted from your twelvedata_api.py
def tickers_list_creator():
    """Get the list of tickers from stocks_details.json"""
    try:
        tickers_file = os.path.join(DATA_DIR, "stocks_details.json")
        with open(tickers_file, "r") as ticker_file:
            tickers = json.load(ticker_file)
            return list(tickers.keys())
    except Exception as e:
        logger.error(f"Error loading tickers: {e}")
        # Fallback to a default list of common S&P 500 stocks
        return ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "JPM", "JNJ", "V", "PG", 
                "NVDA", "HD", "MA", "UNH", "BAC", "DIS", "ADBE", "CRM", "NFLX", "XOM"]

# Preload necessary files
def load_data():
    """Load all necessary data files for the optimizer"""
    try:
        data = {}
        
        # Load correlation matrix
        corr_matrix_path = os.path.join(DATA_DIR, "correlation_matrix.csv")
        data["correlation_matrix"] = pd.read_csv(corr_matrix_path, index_col=0)
        
        # Load scaled geometric mean returns
        geo_means_path = os.path.join(DATA_DIR, "scaled_geometric_mean.json")
        with open(geo_means_path, "r") as file:
            data["geo_means"] = json.load(file)
        
        # Load ESG scores
        esg_scores_path = os.path.join(DATA_DIR, "ESG_Scores.json")
        with open(esg_scores_path, "r") as file:
            data["esg_scores"] = json.load(file)
            
        # Load stock prices for historical data
        stock_prices_path = os.path.join(DATA_DIR, "stock_prices.json")
        with open(stock_prices_path, "r") as file:
            data["stock_prices"] = json.load(file)
            
        # Load SP500 tickers info
        sp500_tickers_path = os.path.join(DATA_DIR, "SA_sp500_tickers.json")
        with open(sp500_tickers_path, "r") as file:
            data["sp500_tickers"] = json.load(file)
            
        logger.info("All data files loaded successfully")
        return data
        
    except Exception as e:
        logger.error(f"Error loading data files: {e}")
        return None

# Function from your simulation.py
def weighted_mean_correlation(correlation_matrix, weights):
    """Calculate the weighted mean correlation of a portfolio"""
    # Convert weights dict to a list that matches the correlation matrix order
    tickers = correlation_matrix.index
    weight_array = np.array([weights.get(ticker, 0) for ticker in tickers])
    
    # Normalize weights to sum to 1
    weight_array = weight_array / weight_array.sum()
    
    # Calculate the weighted correlation
    weighted_corr = np.dot(np.dot(weight_array, correlation_matrix), weight_array)
    return weighted_corr

# Function from your portfolio.py
def portfolio_geometric_mean(data, new_weights):
    """Calculate the portfolio's weighted geometric mean return"""
    lst = []
    for ticker, weight in new_weights.items():
        # Skip if ticker not in data
        if ticker not in data:
            continue
        ret = data[ticker]
        weighted_geometric_mean = ret * weight
        lst.append(weighted_geometric_mean)
    
    return sum(lst)

# Your main algorithm
def suggest_stocks(current_inv, investment_amount, all_data):
    """
    Suggest stocks to add to a portfolio for optimal diversification
    
    Parameters:
    - current_inv: dict {ticker: amount_invested}
    - investment_amount: float (new money to be invested)
    - all_data: dict containing all preloaded data
    
    Returns:
    - dict containing suggestion details
    """
    try:
        # Get data
        corr_matrix = all_data["correlation_matrix"]
        geo_means_dict = all_data["geo_means"]
        esg_scores = all_data["esg_scores"]
        
        # Get list of all available stocks
        ALL_STOCKS = tickers_list_creator()
        
        # Current portfolio information
        current_tickers = list(current_inv.keys())
        current_amounts = np.array(list(current_inv.values()))
        
        # Determine possible additions
        if len(current_tickers) <= 1:
            possible_additions = [stock for stock in ALL_STOCKS 
                                 if stock not in current_inv 
                                 and stock in corr_matrix.index][:30]  # Limit to first 30 for performance
        else:
            possible_additions = [stock for stock in ALL_STOCKS 
                                 if stock not in current_inv 
                                 and stock in corr_matrix.index][:50]  # Limit to first 50 for performance
        
        best_combination = None
        best_sharpe = 0
        best_correlation = 1  # Initialize to highest possible correlation
        best_return = 0
        best_ticker_details = {}
        
        # Track the top 3 suggestions
        top_suggestions = []
        
        for new_stock in possible_additions:
            # Skip if new stock is not in correlation matrix
            if new_stock not in corr_matrix.index:
                continue
                
            new_tickers = current_tickers + [new_stock]
            
            # Ensure all tickers in new_tickers are in correlation matrix
            if not all(ticker in corr_matrix.index for ticker in new_tickers):
                continue
            
            # Compute new weights
            new_amounts = np.append(current_amounts, investment_amount)
            new_weights = {ticker: float(amt / new_amounts.sum()) 
                          for ticker, amt in zip(new_tickers, new_amounts)}
            
            # Extract sub-matrix (only if all tickers are in the correlation matrix)
            try:
                sub_corr_matrix = corr_matrix.loc[new_tickers, new_tickers]
            except KeyError:
                continue
            
            # Compute weighted mean correlation
            try:
                total_mean_corr = weighted_mean_correlation(sub_corr_matrix, new_weights)
                
                # Skip if correlation can't be calculated properly
                if np.isnan(total_mean_corr) or total_mean_corr <= 0:
                    continue
                    
                # Calculate portfolio return
                total_mean_return = portfolio_geometric_mean(geo_means_dict, new_weights)
                
                # Calculate Sharpe ratio (simplified)
                sharpe_ratio = total_mean_return / total_mean_corr
                
                # Get company details
                sp500_data = all_data.get("sp500_tickers", {})
                company_name = sp500_data.get(new_stock, {}).get("company_name", new_stock)
                company_details = {
                    "ticker": new_stock,
                    "company_name": company_name,
                    "current_price": sp500_data.get(new_stock, {}).get("stock_price", "N/A"),
                    "market_cap": sp500_data.get(new_stock, {}).get("market_cap", "N/A"),
                    "sharpe_ratio": float(sharpe_ratio),
                    "correlation": float(total_mean_corr),
                    "expected_return": float(total_mean_return)
                }
                
                # Track this as a potential suggestion
                top_suggestions.append({
                    "ticker": new_stock,
                    "sharpe_ratio": float(sharpe_ratio),
                    "correlation": float(total_mean_corr),
                    "expected_return": float(total_mean_return),
                    "details": company_details
                })
                
                # Update best if this is better
                if abs(sharpe_ratio) > abs(best_sharpe):
                    best_sharpe = sharpe_ratio
                    best_combination = new_stock
                    best_correlation = total_mean_corr
                    best_return = total_mean_return
                    best_ticker_details = company_details
                
            except Exception as e:
                logger.error(f"Error calculating for {new_stock}: {e}")
                continue
        
        # Sort the suggestions by Sharpe ratio
        top_suggestions.sort(key=lambda x: abs(x["sharpe_ratio"]), reverse=True)
        top_suggestions = top_suggestions[:3]  # Keep only top 3
        
        # If no valid suggestions were found
        if not best_combination:
            return {
                "status": "error",
                "message": "Could not find a suitable stock to add to your portfolio."
            }
        
        # Compute weighted ESG score for the current portfolio
        current_esg_score = 0
        for ticker in current_tickers:
            ticker_weight = current_inv[ticker] / sum(current_inv.values())
            esg_value = 0
            
            # Get ESG score
            if ticker in esg_scores:
                if isinstance(esg_scores[ticker], dict) and "totalEsg" in esg_scores[ticker]:
                    esg_value = esg_scores[ticker]["totalEsg"]
                elif isinstance(esg_scores[ticker], dict) and "esgScores" in esg_scores[ticker]:
                    esg_value = esg_scores[ticker]["esgScores"].get("totalEsg", 0)
            
            current_esg_score += ticker_weight * esg_value
        
        # Compute weighted ESG score for the new portfolio
        new_portfolio_inv = {**current_inv, best_combination: investment_amount}
        new_esg_score = 0
        
        for ticker, amount in new_portfolio_inv.items():
            ticker_weight = amount / sum(new_portfolio_inv.values())
            esg_value = 0
            
            # Get ESG score
            if ticker in esg_scores:
                if isinstance(esg_scores[ticker], dict) and "totalEsg" in esg_scores[ticker]:
                    esg_value = esg_scores[ticker]["totalEsg"]
                elif isinstance(esg_scores[ticker], dict) and "esgScores" in esg_scores[ticker]:
                    esg_value = esg_scores[ticker]["esgScores"].get("totalEsg", 0)
            
            new_esg_score += ticker_weight * esg_value
        
        # Create response
        response = {
            "status": "success",
            "suggestion": {
                "ticker": best_combination,
                "details": best_ticker_details,
                "sharpe_ratio": float(best_sharpe),
                "correlation": float(best_correlation),
                "expected_return": float(best_return),
                "investment_amount": float(investment_amount)
            },
            "esg": {
                "current_score": float(current_esg_score),
                "new_score": float(new_esg_score),
                "change": float(new_esg_score - current_esg_score)
            },
            "alternatives": top_suggestions
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error in suggest_stocks: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple endpoint to check if API is running"""
    return jsonify({"status": "healthy"})

@app.route('/api/tickers', methods=['GET'])
def get_tickers():
    """Get list of available tickers"""
    tickers = tickers_list_creator()
    return jsonify({"tickers": tickers})

@app.route('/api/analyze', methods=['POST'])
def analyze_portfolio():
    """Analyze a portfolio and suggest optimal additions"""
    try:
        # Get JSON data from request
        data = request.json
        
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # Extract current investments and new investment amount
        current_inv = data.get('current_investments', {})
        investment_amount = float(data.get('investment_amount', 1000))
        
        # Load all necessary data
        all_data = load_data()
        if not all_data:
            return jsonify({
                "status": "error", 
                "message": "Could not load necessary data files"
            }), 500
        
        # Run the optimization algorithm
        result = suggest_stocks(current_inv, investment_amount, all_data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_portfolio: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Preload data at startup
    app.run(debug=True, host='0.0.0.0', port=5000)
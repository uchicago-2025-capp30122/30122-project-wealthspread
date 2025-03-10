import json
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

def plot_stock_history(symbol):
    """
    Plot historical stock data with simulated historical prices if no cached data exists.
    
    Parameters:
    symbol (str): Stock symbol (e.g., 'AAPL')
    """
    try:
        # Simulate historical data if no cached file exists
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*5)  # 5 years of data
        
        # Get current stock data for initial price reference
        stock_data = get_stock_data(symbol)
        current_price = float(stock_data.get('stock_price', '100').replace('$', ''))
        
        # Generate simulated price data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Simulate price movement with some volatility
        beta = stock_data.get('beta', 1.0)
        volatility = 0.02 * beta  # Adjust volatility based on beta
        
        # Start with current price and simulate random walk
        prices = [current_price]
        for _ in range(len(dates) - 1):
            change = random.normalvariate(0, volatility * prices[-1])
            new_price = max(prices[-1] + change, 1)  # Prevent negative prices
            prices.append(new_price)
        
        # Create DataFrame
        df = pd.DataFrame({
            'datetime': dates,
            'close': prices,
            'high': [p * 1.02 for p in prices],  # Slight variation for high
            'low': [p * 0.98 for p in prices]    # Slight variation for low
        })
        
        # Compute some basic statistics
        current_price = df['close'].iloc[-1]
        high_price = df['high'].max()
        low_price = df['low'].min()
        avg_price = df['close'].mean()
        
        plt.figure(figsize=(15, 8))
        
        # Plot closing price
        plt.plot(df['datetime'], df['close'], label='Closing Price', color='blue')
        
        # Add price range as shaded area
        plt.fill_between(df['datetime'], df['low'], df['high'], 
                        alpha=0.2, color='blue', label='Price Range')
        
        plt.title(f'{symbol} Stock Price History (Simulated 5-Year Data)', fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10)
        
        plt.xticks(rotation=45)
        
        # Add statistics text box
        stats_text = (
            f'Statistics:\n'
            f'Current Price: ${current_price:.2f}\n'
            f'5-Year High: ${high_price:.2f}\n'
            f'5-Year Low: ${low_price:.2f}\n'
            f'Average Price: ${avg_price:.2f}'
        )
        
        plt.text(0.02, 0.98, stats_text,
                transform=plt.gca().transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round',
                         facecolor='white',
                         alpha=0.8),
                fontsize=10)
        
        # Calculate price range for y-axis padding
        price_range = high_price - low_price
        plt.ylim(low_price - price_range*0.1, high_price + price_range*0.1)
        
        plt.tight_layout()
        
        # Ensure Visualization Example directory exists
        import os
        vis_dir = os.path.join('wealthspread', 'Visualization Example')
        os.makedirs(vis_dir, exist_ok=True)
        
        # Save the plot
        output_path = os.path.join(vis_dir, f'{symbol}_history.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()  # Close the plot to free up memory
        
        print(f"Plot saved as {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error generating visualization for {symbol}: {e}")
        return None

def get_stock_data(ticker):
    """
    Get stock data (copied from the main script to ensure this works standalone)
    """
    # Reuse the get_stock_data implementation from the main script
    common_sectors = {
        'AAPL': 'Technology', 'MSFT': 'Technology', 'GOOGL': 'Technology', 
        'AMZN': 'Consumer Cyclical', 'META': 'Technology', 'TSLA': 'Automotive',
        'JPM': 'Financial Services', 'V': 'Financial Services', 'PG': 'Consumer Defensive',
        'NVDA': 'Technology', 'HD': 'Consumer Cyclical', 'UNH': 'Healthcare',
        'JNJ': 'Healthcare', 'MA': 'Financial Services', 'BAC': 'Financial Services',
        'DIS': 'Communication Services', 'ADBE': 'Technology', 'CRM': 'Technology',
        'NFLX': 'Communication Services', 'CMCSA': 'Communication Services',
        'XOM': 'Energy', 'VZ': 'Communication Services', 'INTC': 'Technology',
        'CSCO': 'Technology', 'PFE': 'Healthcare', 'ABT': 'Healthcare',
        'KO': 'Consumer Defensive', 'PEP': 'Consumer Defensive', 'MRK': 'Healthcare',
        'WMT': 'Consumer Defensive', 'T': 'Communication Services', 'CVX': 'Energy',
        'MCD': 'Consumer Cyclical', 'NKE': 'Consumer Cyclical', 'WFC': 'Financial Services',
        'ABBV': 'Healthcare', 'ORCL': 'Technology', 'AVGO': 'Technology',
        'ACN': 'Technology'
    }
    
    company_names = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        # ... (rest of the company names from the original script)
    }
    
    stock_data = {
        'company_name': company_names.get(ticker, f"{ticker} Inc."),
        'sector': common_sectors.get(ticker, 'General'),
        'market_cap': f"${random.randint(10, 2000)}B",
        'stock_price': f"${random.randint(50, 500)}",
        'pct_change': f"{random.uniform(-2.0, 2.0):.2f}%",
        'revenue': f"${random.randint(1, 500)}B",
        'beta': round(random.uniform(0.5, 2.0), 2),
        'avg_return': round(random.uniform(0.03, 0.25), 3),
        'volatility': round(random.uniform(0.1, 0.4), 3),
        'esg_score': round(random.uniform(10, 40), 1)
    }
    
    return stock_data

# Example usage
if __name__ == "__main__":
    plot_stock_history('AAPL')
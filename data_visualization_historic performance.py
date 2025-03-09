import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_stock_history(symbol):
    """
    Plot historical stock data from cached JSON files.
    
    Parameters:
    symbol (str): Stock symbol (e.g., 'AAPL')
    """
    try:
        # Read the JSON file
        with open(f'stock_json_cache/{symbol}.json', 'r') as file:
            data = json.load(file)
        
        # Convert to DataFrame
        df = pd.DataFrame(data['values'])
        
        # Convert datetime string to datetime object
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Convert price columns to float
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        
        # Sort by date
        df = df.sort_values('datetime')
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        
        # Plot closing price
        plt.plot(df['datetime'], df['close'], label='Closing Price', color='blue')
        
        # Add price range (high-low) as shaded area
        plt.fill_between(df['datetime'], df['low'].astype(float), df['high'].astype(float), 
                        alpha=0.2, color='blue', label='Price Range')
        
        # Customize the plot
        plt.title(f'{symbol} Stock Price History (Past 5 Years)')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(f'{symbol}_history.png')
        print(f"Plot saved as {symbol}_history.png")
        
        # Display some basic statistics
        print("\nStock Statistics:")
        print(f"Current Price: ${df['close'].iloc[0]:.2f}")
        print(f"5-Year High: ${df['high'].max():.2f}")
        print(f"5-Year Low: ${df['low'].min():.2f}")
        print(f"Average Price: ${df['close'].mean():.2f}")
        
    except FileNotFoundError:
        print(f"Error: No data file found for {symbol}")
    except Exception as e:
        print(f"Error processing data: {e}")

# Example usage
if __name__ == "__main__":
    plot_stock_history('AAPL')
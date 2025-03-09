import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_stock_history(symbol):
    """
    Plot historical stock data from cached JSON files with statistics on the plot.
    
    Parameters:
    symbol (str): Stock symbol (e.g., 'AAPL')
    """
    try:
        # Read the JSON file
        with open(f'company_info/{symbol}.json', 'r') as file:
            data = json.load(file)
        
        # Convert to DataFrame
        df = pd.DataFrame(data['values'])
        
        # Convert datetime string to datetime object
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Convert price columns to float
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        
        # Sort data by date
        df = df.sort_values('datetime')
        
        # Compute some basic statistics to be displayed on the plot 
        current_price = df['close'].iloc[0]
        high_price = df['high'].max()
        low_price = df['low'].min()
        avg_price = df['close'].mean()
        
        
        plt.figure(figsize=(15, 8)) # Specify plot size i.e size of the rendered PNg file 
        
        
        # Plot closing price
        plt.plot(df['datetime'], df['close'], label='Closing Price', color='blue')
        
        # Add price range (high-low) as shaded area
        plt.fill_between(df['datetime'], df['low'].astype(float), df['high'].astype(float), 
                        alpha=0.2, color='blue', label='Price Range')
        
        # Optimizing the output to meet display requirements
        plt.title(f'{symbol} Stock Price History (Past 5 Years)', fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10)
        
        
        plt.xticks(rotation=45) # Rotate x-axis labels for a cleaner rendering

        
        # Add statistics text box to be displayed on the rendered plot 
        stats_text = (
            f'Statistics:\n'
            f'Current Price: ${current_price:.2f}\n'
            f'5-Year High: ${high_price:.2f}\n'
            f'5-Year Low: ${low_price:.2f}\n'
            f'Average Price: ${avg_price:.2f}'
        )
        
        # Add Textbox position (LEFT)
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
        
        plt.tight_layout() # Adjust layout to prevent label cutoff
        
        # Save
        plt.savefig(f'{symbol}_history.png', dpi=300, bbox_inches='tight')
        print(f"Plot saved as {symbol}_history.png")
        
        # Display
        plt.show()
        
    except FileNotFoundError:
        print(f"Error: No data file found for {symbol}")
    except Exception as e:
        print(f"Error processing data: {e}")

# Example usage, you can input any other SP500 stock, e.g. MSFT (Microsoft), NFLX (Netflix), AMZN (Amazon)
if __name__ == "__main__":
    plot_stock_history('BA')
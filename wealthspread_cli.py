#!/usr/bin/env python3
"""
Wealth Spread: Interactive CLI for Intelligent Portfolio Diversification
"""

import os
import sys
import json
from pathlib import Path
import random
from wealthspread.correlation.twelvedata_api import tickers_list_creator


ALL_STOCKS = tickers_list_creator()

# Get project root and set up paths
project_root = Path(__file__).parent.absolute()

# Add the correlation directory directly to the path
correlation_path = project_root / "wealthspread" / "correlation"
sys.path.insert(0, str(correlation_path))

# Import the portfolio module directly
import wealthspread.correlation.portfolio


# Define file paths
ESG_SCORES_PATH = project_root / "wealthspread" / "esg" / "ESG_Scores.json"
COMPANY_INFO_PATH = project_root / "wealthspread" / "scrape" / "company_info.json"

# Common tickers for better UX
SAMPLE_TICKERS = ALL_STOCKS

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    clear_screen()
    print("\n" + "=" * 90)
    print("""
    __      __              .__   __   .__                                             __
   /  \    /  \____   ____  |  |_/  |_ |  |__   ________ __ _______  ____________   __ | |
   \   \/\/   /    \_/  _ \ |  |\   __\\|  |  \ /  ___/     \\_  __ \ /    \_/  _ \  /  __ |
    \        (   ^__)  |_\ ||  |_|  |  |   Y  \\___ \|  |  / |  | \/(   ^__)  |_\ |/  /_/ |
     \__/\__/ \____/|_____,_|____|__|  |__/___|______)   /  |__|    \____/|_____,_\_____|
                                                     |__|            
   Intelligent Portfolio Diversification Tool
   """)
    print("=" * 90 + "\n")

def load_json_file(filepath):
    """Load a JSON file and return the data"""
    with open(filepath, 'r') as f:
        return json.load(f)


def input_with_validation(prompt, validator=None, error_message=None):
    """Get user input with validation"""
    while True:
        user_input = input(prompt).strip()
        if validator is None or validator(user_input):
            return user_input
        print(error_message or "Invalid input. Please try again.")

def is_valid_amount(amount_str):
    """Validate if the input is a valid monetary amount"""
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False

def ticker_validator(ticker):
    "Validates if the tickers is from the S&P 500"
    return ticker.upper() in ALL_STOCKS

def get_current_portfolio():
    """Interactively get the user's current portfolio"""
    print("\n=== CURRENT PORTFOLIO ===")
    print("Let's start by creating your current portfolio (2-5 stocks).\n")
    
    portfolio = {}
    min_stocks = 2
    max_stocks = 5
    
    # Get number of stocks
    num_stocks = input_with_validation(
        f"How many stocks do you currently have in your portfolio? ({min_stocks}-{max_stocks}): ",
        lambda x: x.isdigit() and min_stocks <= int(x) <= max_stocks,
        f"Please enter a number between {min_stocks} and {max_stocks}."
    )
    num_stocks = int(num_stocks)
    
    # Show some sample tickers
    print("\nSample tickers for reference:")
    sample_display = ", ".join(random.sample(ALL_STOCKS, 15))
    print(f"  {sample_display}, ...")
    
    # Get each stock ticker and amount
    for i in range(1, num_stocks + 1):
        print(f"\nStock #{i}:")
        
        # Get ticker
        ticker = input_with_validation(
            "Enter ticker symbol (e.g., AAPL): ",
            ticker_validator,
            "Ticker not found. Please enter a valid ticker FROM S&P 500."
        ).upper()
        
        # Get amount invested
        amount = input_with_validation(
            f"Enter amount invested in {ticker} ($): ",
            is_valid_amount,
            "Please enter a valid positive amount."
        )
        amount = float(amount)
        
        portfolio[ticker] = amount
    
    return portfolio

def get_additional_investment():
    """Get the amount the user wants to invest additionally"""
    print("\n=== ADDITIONAL INVESTMENT ===")
    amount = input_with_validation(
        "Enter the additional amount you want to invest ($): ",
        is_valid_amount,
        "Please enter a valid positive amount."
    )
    return float(amount)

def analyze_portfolio():
    """Complete workflow for getting portfolio suggestions"""
    print_header()
    
    try:
        user_portfolio = get_current_portfolio()
        investment_amount = get_additional_investment()
        
        print("\nYour current portfolio:")
        for ticker, amount in user_portfolio.items():
            print(f"  {ticker}: ${amount:.2f}")
        print(f"Additional investment: ${investment_amount:.2f}")
        
        while True:
            proceed = input("\nAnalyze this portfolio for suggestions? (y/n): ").lower().strip()
            if proceed == 'y':
                print("\nAnalyzing portfolio... (this may take a moment)")
                
                try:
                    # Call the suggest_stocks_sharpe function from portfolio module
                    result = wealthspread.correlation.portfolio.suggest_stocks_sharpe(user_portfolio, investment_amount)
                    with open(COMPANY_INFO_PATH, 'r') as file:
                          data = json.load(file)

                    # Preview results in an appealing way
                    print("\n=== ANALYSIS RESULTS ===")
                    print("\n" + "="*50)
                    print("📈 Portfolio Diversification Suggestion 📈")
                    print("="*50)
                    print(f"\n🎯 **Recommended Stock to Add:** {result[0]}")
                    print(f"\n🚀 **Optimized Sharpe Ratio:** {result[1]}")
                    print(f"🔗 **Average Portfolio Correlation:** {result[2]}")
                    print(f"\n🌿 **Current ESG Score:** {result[3]}")
                    print(f"🌱 **New ESG Score (after addition):** {result[4]}")                    
                    print("\n✨ Happy Investing! ✨")
                    print("\n--- Company Information ---")
                    print(f"\n**About Company:**\n{data[result[0]]['about_company']}")
                    print("\n--- Financial Performance ---")
                    print(f"\n**Financials:**\n{data[result[0]]['fin_performance']}")
                    print("="*50 + "\n")
                    
                except Exception as e:
                    print(f"\nError analyzing portfolio: {str(e)}")
                    print("Please try again with different stocks.")
                
                break
            elif proceed == 'n':
                print("\nReturning to main menu...")
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    except Exception as e:
        print(f"\nError setting up portfolio: {str(e)}")
    
    input("\nPress Enter to continue...")

def get_esg_info():
    """Get and display ESG information for a specific ticker"""
    print_header()
    print("=== ESG INFORMATION ===")
    
    # Show sample tickers
    print("Sample tickers for reference:")
    sample_display = ", ".join(random.sample(ALL_STOCKS, 15))
    print(f"  {sample_display}, ...")
    
    ticker = input_with_validation(
        "\nEnter ticker symbol to get ESG information (e.g., AAPL): ",
        lambda x: len(x) > 0 and len(x) <= 5,
        "Please enter a valid ticker symbol (1-5 characters)."
    ).upper()
    
    try:
        # Load ESG data and company info
        esg_scores = load_json_file(ESG_SCORES_PATH)
        company_info = load_json_file(COMPANY_INFO_PATH)
        
        # Display company information
        print(f"\n=== COMPANY AND ESG INFORMATION FOR {ticker} ===\n")
        
        # Company information
        if ticker in company_info:
            info = company_info[ticker]
            print("COMPANY INFORMATION:")
            
            # Extract about company data
            about_text = info.get('about_company', '')
            about_summary = about_text.split('[Read more]')[0] if '[Read more]' in about_text else about_text
            print(f"- About: {about_summary}")
            
            # Look for industry and sector info
            if 'Industry ' in about_text:
                industry = about_text.split('Industry ')[1].split(' Sector')[0].strip()
                print(f"- Industry: {industry}")
                
            if 'Sector ' in about_text:
                sector = about_text.split('Sector ')[1].split(' IPO')[0].strip()
                print(f"- Sector: {sector}")
                
            # Extract financial performance
            fin_performance = info.get('fin_performance', '')
            if fin_performance:
                print(f"- Financial Performance: {fin_performance}")
        else:
            print(f"No detailed company information available for {ticker}.")
        
        # ESG information
        print("\nESG INFORMATION:")
        
        if ticker in esg_scores:
            esg = esg_scores[ticker]
            
            # Check if ESG data is a dictionary
            if isinstance(esg, dict):
                total_esg = esg.get('totalEsg', 'N/A')
                env_score = esg.get('environmentScore', 'N/A')
                social_score = esg.get('socialScore', 'N/A')
                gov_score = esg.get('governanceScore', 'N/A')
                
                print(f"- Total ESG Score: {total_esg}")
                print(f"- Environmental Score: {env_score}")
                print(f"- Social Score: {social_score}")
                print(f"- Governance Score: {gov_score}")
                
                # Determine risk level
                if isinstance(total_esg, (int, float)):
                    if total_esg <= 15:
                        risk_level = "Low risk (excellent)"
                    elif total_esg <= 25:
                        risk_level = "Medium risk (average)"
                    else:
                        risk_level = "High risk (concerning)"
                    print(f"- Risk Level: {risk_level}")
            else:
                print(f"ESG data for {ticker} is not in the expected format.")
        else:
            print(f"No ESG information available for {ticker}.")
    
    except Exception as e:
        print(f"\nError getting ESG information: {str(e)}")
    
    input("\nPress Enter to continue...")

def show_main_menu():
    """Display the main menu and get user choice"""
    print_header()
    print("MAIN MENU")
    print("1. Analyze Portfolio & Get Stock Suggestions")
    print("2. Get ESG Information for a Ticker")
    print("3. Exit")
    
    choice = input_with_validation(
        "\nEnter your choice (1-3): ",
        lambda x: x.isdigit() and 1 <= int(x) <= 3,
        "Please enter a number between 1 and 3."
    )
    
    return int(choice)

def main():
    """Main entry point for the interactive CLI"""
    try:
        while True:
            choice = show_main_menu()
            
            if choice == 1:
                analyze_portfolio()
            elif choice == 2:
                get_esg_info()
            elif choice == 3:
                print("\nThank you for using Wealth Spread! Goodbye.")
                break
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

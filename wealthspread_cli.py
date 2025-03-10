#!/usr/bin/env python3
"""
Wealth Spread: Interactive CLI for Intelligent Portfolio Diversification
Standalone version that doesn't rely on external files
"""

import os
import sys
import json
import time
import random
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wealth_spread.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("wealth_spread")

# Sample SP500 tickers for demo purposes
SAMPLE_SP500 = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "BRK.B", "JPM", "V", "PG",
    "NVDA", "HD", "UNH", "JNJ", "MA", "BAC", "DIS", "ADBE", "CRM", "NFLX",
    "CMCSA", "XOM", "VZ", "INTC", "CSCO", "PFE", "ABT", "KO", "PEP", "MRK",
    "WMT", "T", "CVX", "MCD", "NKE", "WFC", "ABBV", "ORCL", "AVGO", "ACN"
]

# Path handling for data files
def get_data_file_path(filename):
    """Get the absolute path to a data file, checking multiple possible locations"""
    # Handle path strings or Path objects
    filename_path = Path(filename)
    
    # Try in the current directory
    if filename_path.exists():
        return str(filename_path.absolute())
    
    # Try in the script's directory
    script_dir = Path(__file__).parent.absolute()
    script_dir_path = script_dir / filename_path
    if script_dir_path.exists():
        return str(script_dir_path)
    
    # Try from project root (assuming we're in the project root or a subdirectory)
    for parent in [Path("."), script_dir, script_dir.parent]:
        # Try direct path
        direct_path = parent / filename_path
        if direct_path.exists():
            return str(direct_path.absolute())
        
        # Try in common subdirectories
        for subdir in ["wealthspread", "correlation", "scrape", "Visualization Example"]:
            subdir_path = parent / subdir / filename_path
            if subdir_path.exists():
                return str(subdir_path.absolute())
            
            # Try deeper paths for nested structure
            nested_path = parent / "wealthspread" / subdir / filename_path
            if nested_path.exists():
                return str(nested_path.absolute())
    
    # Try the exact 30122-project-wealthspread path
    project_path = Path("30122-project-wealthspread") / filename_path
    if project_path.exists():
        return str(project_path.absolute())
    
    # Try within 30122-project-wealthspread/wealthspread
    project_ws_path = Path("30122-project-wealthspread") / "wealthspread" / filename_path
    if project_ws_path.exists():
        return str(project_ws_path.absolute())
    
    # If we get here, the file wasn't found
    logger.warning(f"Could not find data file: {filename}")
    return None

def get_company_info(ticker):
    """Get company information from company_info.json file"""
    # Cache for company info
    if not hasattr(get_company_info, "cache"):
        get_company_info.cache = {}
        
        # Try to load the company_info.json file
        try:
            company_file_path = get_data_file_path("company_info.json")
            if company_file_path:
                with open(company_file_path, 'r') as f:
                    get_company_info.cache = json.load(f)
                logger.info(f"Loaded company info from {company_file_path}")
            else:
                logger.warning("Could not find company_info.json. Using fallback data.")
        except Exception as e:
            logger.error(f"Error loading company_info.json: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Get stock details for additional info
    stock_details = get_stock_data(ticker)
    
    # Prepare a default result
    result = {
        'name': stock_details.get('company_name', f"{ticker}"),
        'description': f"A company in the {stock_details.get('sector', 'Unknown')} sector.",
        'industry': stock_details.get('sector', 'Unknown'),
        'revenue': stock_details.get('revenue', "Unknown")
    }
    
    # If ticker exists in the company info data, extract relevant information
    if ticker in get_company_info.cache:
        company_data = get_company_info.cache[ticker]
        
        # Extract about company data (contains most of our needed information)
        about_text = company_data.get('about_company', '')
        
        # Parse industry, sector from the about text if available
        industry = "Unknown"
        sector = "Unknown"
        
        # Look for industry and sector info
        if 'Industry ' in about_text:
            industry_part = about_text.split('Industry ')[1].split(' Sector')[0]
            industry = industry_part.strip()
            
        if 'Sector ' in about_text:
            sector_part = about_text.split('Sector ')[1].split(' IPO')[0]
            sector = sector_part.strip()
            
        # Extract other potential information like IPO date, country, etc.
        founded = None
        if 'IPO Date ' in about_text:
            founded_part = about_text.split('IPO Date ')[1].split(' Country')[0]
            founded = founded_part.strip()
            
        country = None
        if 'Country ' in about_text:
            country_part = about_text.split('Country ')[1].split(' Stock')[0]
            country = country_part.strip()
            
        # Extract financial performance
        fin_performance = company_data.get('fin_performance', '')
        
        # Create result
        result = {
            'name': stock_details.get('company_name', f"{ticker}"),
            'description': about_text.split('[Read more]')[0] if '[Read more]' in about_text else about_text,
            'industry': industry,
            'sector': sector,
            'founded': founded,
            'headquarters': country,
            'revenue': stock_details.get('revenue', "Unknown"),
            'market_cap': stock_details.get('market_cap', "Unknown"),
            'performance': fin_performance
        }
    
    return result

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    clear_screen()
    print("\n" + "=" * 80)
    print("""
     __      __            .__   __   .__                                           .___
    /  \    /  \___________|  |_/  |_ |  |__   ________ ______ _______   ____    __| _/
    \   \/\/   /  _ \_  __ \  |\   __\|  |  \ /  ___/  |  \__  \\_  __ \ /    \  / __ | 
     \        (  <_> )  | \/  |_|  |  |   Y  \\___ \|  |  // __ \|  | \/|   |  \/ /_/ | 
      \__/\  / \____/|__|  |____/__|  |___|  /____  >____/(____  /__|   |___|  /\____ | 
           \/                              \/     \/           \/            \/      \/ 
    Intelligent Portfolio Diversification Tool
    """)
    print("=" * 80 + "\n")

def input_with_validation(prompt, validator=None, error_message=None):
    """Get user input with validation"""
    while True:
        user_input = input(prompt).strip()
        if validator is None or validator(user_input):
            return user_input
        print(error_message or "Invalid input. Please try again.")

def is_valid_ticker(ticker):
    """Validate if a ticker is in our sample list"""
    return ticker.upper() in SAMPLE_SP500

def suggest_ticker(portfolio_tickers):
    """Suggest a new ticker not in the current portfolio"""
    available_tickers = [t for t in SAMPLE_SP500 if t not in portfolio_tickers]
    if not available_tickers:
        return SAMPLE_SP500[0]  # Just in case
    return random.choice(available_tickers)

def is_valid_amount(amount_str):
    """Validate if the input is a valid monetary amount"""
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False

def get_stock_data(ticker):
    """Get stock data from the stocks_details.json file"""
    # Cache for stock data
    if not hasattr(get_stock_data, "cache"):
        get_stock_data.cache = {}
        
        # Try to load the stocks_details.json file
        try:
            stocks_file_path = get_data_file_path("stocks_details.json")
            if stocks_file_path:
                with open(stocks_file_path, 'r') as f:
                    get_stock_data.cache = json.load(f)
                logger.info(f"Loaded stock data from {stocks_file_path}")
            else:
                logger.warning("Could not find stocks_details.json. Using fallback data.")
        except Exception as e:
            logger.error(f"Error loading stocks_details.json: {e}")
    
    # If ticker is not in our data, generate random data for it
    if ticker not in get_stock_data.cache:
        # Common sectors for major companies
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
        
        # Common company names
        company_names = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'META': 'Meta Platforms Inc.',
            'TSLA': 'Tesla Inc.',
            'BRK.B': 'Berkshire Hathaway Inc.',
            'JPM': 'JPMorgan Chase & Co.',
            'V': 'Visa Inc.',
            'PG': 'Procter & Gamble Co.',
            'NVDA': 'NVIDIA Corporation',
            'HD': 'Home Depot Inc.',
            'UNH': 'UnitedHealth Group Inc.',
            'JNJ': 'Johnson & Johnson',
            'MA': 'Mastercard Inc.',
            'BAC': 'Bank of America Corp.',
            'DIS': 'Walt Disney Co.',
            'ADBE': 'Adobe Inc.',
            'CRM': 'Salesforce Inc.',
            'NFLX': 'Netflix Inc.',
            'CMCSA': 'Comcast Corporation',
            'XOM': 'Exxon Mobil Corporation',
            'VZ': 'Verizon Communications Inc.',
            'INTC': 'Intel Corporation',
            'CSCO': 'Cisco Systems Inc.',
            'PFE': 'Pfizer Inc.',
            'ABT': 'Abbott Laboratories',
            'KO': 'Coca-Cola Co.',
            'PEP': 'PepsiCo Inc.',
            'MRK': 'Merck & Co. Inc.',
            'WMT': 'Walmart Inc.',
            'T': 'AT&T Inc.',
            'CVX': 'Chevron Corporation',
            'MCD': 'McDonald\'s Corporation',
            'NKE': 'Nike Inc.',
            'WFC': 'Wells Fargo & Co.',
            'ABBV': 'AbbVie Inc.',
            'ORCL': 'Oracle Corporation',
            'AVGO': 'Broadcom Inc.',
            'ACN': 'Accenture plc'
        }
        
        get_stock_data.cache[ticker] = {
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
    
    return get_stock_data.cache[ticker]

def get_esg_scores(ticker):
    """Get ESG scores from ESG_Scores.json file if available"""
    if not hasattr(get_esg_scores, "cache"):
        get_esg_scores.cache = {}
        
        # Try to load the ESG_Scores.json file
        try:
            esg_file_path = get_data_file_path("ESG_Scores.json")
            if esg_file_path:
                with open(esg_file_path, 'r') as f:
                    get_esg_scores.cache = json.load(f)
                logger.info(f"Loaded ESG data from {esg_file_path}")
            else:
                logger.warning("Could not find ESG_Scores.json. Using fallback data.")
        except Exception as e:
            logger.error(f"Error loading ESG_Scores.json: {e}")
    
    # Return ESG data if available, otherwise calculate from stock data
    if ticker in get_esg_scores.cache:
        esg_data = get_esg_scores.cache[ticker]
        # Map the field names to our expected format
        return {
            'total': esg_data.get('totalEsg', 0),
            'environmental': esg_data.get('environmentScore', 0),
            'social': esg_data.get('socialScore', 0),
            'governance': esg_data.get('governanceScore', 0)
        }
    
    # Fallback to calculating from stock data
    stock_data = get_stock_data(ticker)
    total_esg = stock_data.get('esg_score', round(random.uniform(10, 40), 1))
    env_score = round(total_esg * random.uniform(0.25, 0.45), 1)
    social_score = round(total_esg * random.uniform(0.25, 0.45), 1)
    gov_score = round(total_esg - env_score - social_score, 1)
    
    return {
        'total': total_esg,
        'environmental': env_score,
        'social': social_score,
        'governance': gov_score
    }

def get_correlation_data():
    """Get stock correlation data from correlation_matrix.csv if available"""
    if not hasattr(get_correlation_data, "cache"):
        get_correlation_data.cache = {}
        
        # Try to load the correlation_matrix.csv file
        try:
            correlation_file_path = get_data_file_path("correlation_matrix.csv")
            if correlation_file_path:
                with open(correlation_file_path, 'r') as f:
                    # Simple CSV parsing - assumes first row is headers and first column is tickers
                    lines = f.readlines()
                    headers = lines[0].strip().split(',')
                    for line in lines[1:]:
                        values = line.strip().split(',')
                        ticker = values[0]
                        correlations = {}
                        for i, val in enumerate(values[1:], 1):
                            if i < len(headers):
                                try:
                                    correlations[headers[i]] = float(val)
                                except ValueError:
                                    correlations[headers[i]] = 0.5  # Default if value can't be parsed
                        get_correlation_data.cache[ticker] = correlations
                logger.info(f"Loaded correlation data from {correlation_file_path}")
            else:
                logger.warning("Could not find correlation_matrix.csv. Using fallback data.")
        except Exception as e:
            logger.error(f"Error loading correlation_matrix.csv: {e}")
    
    return get_correlation_data.cache

def get_current_portfolio():
    """Interactively get the user's current portfolio"""
    print("\n=== CURRENT PORTFOLIO ===")
    print("Let's start by creating your current portfolio (1-5 stocks).\n")
    
    portfolio = {}
    min_stocks = 1
    max_stocks = 5
    
    # Get number of stocks
    num_stocks = input_with_validation(
        f"How many stocks do you currently have in your portfolio? ({min_stocks}-{max_stocks}): ",
        lambda x: x.isdigit() and min_stocks <= int(x) <= max_stocks,
        f"Please enter a number between {min_stocks} and {max_stocks}."
    )
    num_stocks = int(num_stocks)
    
    # Get each stock ticker and amount
    for i in range(1, num_stocks + 1):
        print(f"\nStock #{i}:")
        
        # Show available tickers
        print("Sample tickers from S&P 500 (you can enter others as well):")
        sample_display = ", ".join(random.sample(SAMPLE_SP500, min(10, len(SAMPLE_SP500))))
        print(f"  {sample_display}, ...")
        
        # Get ticker
        ticker = input_with_validation(
            "Enter ticker symbol (e.g., AAPL): ",
            lambda x: len(x) > 0 and len(x) <= 5,
            "Please enter a valid ticker symbol (1-5 characters)."
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

def calculate_metrics(portfolio, new_stock_ticker, investment_amount):
    """Calculate portfolio metrics using actual data files when available"""
    # Calculate total portfolio value
    total_current_value = sum(portfolio.values())
    total_new_value = total_current_value + investment_amount
    
    # Get data for current portfolio stocks
    portfolio_data = {ticker: get_stock_data(ticker) for ticker in portfolio}
    new_stock_data = get_stock_data(new_stock_ticker)
    
    # Get correlation data
    correlation_data = get_correlation_data()
    
    # Calculate correlation using actual correlation data if available
    if new_stock_ticker in correlation_data and all(ticker in correlation_data.get(new_stock_ticker, {}) for ticker in portfolio):
        # Use actual correlation data
        correlations = [correlation_data[new_stock_ticker].get(ticker, 0.5) for ticker in portfolio]
        correlation = sum(correlations) / len(correlations) if correlations else 0.5
    else:
        # Fallback to sector-based correlation
        current_sectors = set(data.get('sector', 'Unknown') for data in portfolio_data.values())
        new_sector = new_stock_data.get('sector', 'Unknown')
        sector_diversity = 1 if new_sector not in current_sectors else 0.5
        correlation = round(random.uniform(0.2, 0.7) * (1 - sector_diversity * 0.3), 3)
    
    # Always round correlation for display
    correlation = round(correlation, 3)
    
    # Calculate current portfolio beta and expected return
    weighted_beta = sum(portfolio_data[ticker].get('beta', 1.0) * amount / total_current_value 
                        for ticker, amount in portfolio.items())
    weighted_return = sum(portfolio_data[ticker].get('avg_return', 0.1) * amount / total_current_value 
                          for ticker, amount in portfolio.items())
    
    # Calculate new portfolio beta and expected return
    new_weight = investment_amount / total_new_value
    current_weight = total_current_value / total_new_value
    new_portfolio_beta = (weighted_beta * current_weight) + (new_stock_data.get('beta', 1.0) * new_weight)
    expected_return = (weighted_return * current_weight) + (new_stock_data.get('avg_return', 0.1) * new_weight)
    expected_return = round(expected_return, 3)
    
    # Calculate ESG score
    esg_data = get_esg_scores(new_stock_ticker)
    new_stock_esg = esg_data.get('total', new_stock_data.get('esg_score', 25))
    
    current_esg = 0
    for ticker, amount in portfolio.items():
        ticker_esg = get_esg_scores(ticker)
        current_esg += ticker_esg.get('total', portfolio_data[ticker].get('esg_score', 25)) * amount / total_current_value
    
    new_portfolio_esg = (current_esg * current_weight) + (new_stock_esg * new_weight)
    current_esg = round(current_esg, 1)
    new_portfolio_esg = round(new_portfolio_esg, 1)
    
    # Get sector information, with a fallback
    stock_sector = new_stock_data.get('sector', None)
    # If sector is missing or None, try to get sector from a common sectors dictionary
    if not stock_sector:
        # Common sectors for major companies
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
        stock_sector = common_sectors.get(new_stock_ticker, 'General')
    
    # Calculate Sharpe ratio (higher is better: 0.5-3)
    # Formula: (Expected Return - Risk-Free Rate) / Portfolio Standard Deviation
    # Simplified for demo
    risk_free_rate = 0.03  # 3% as a constant
    portfolio_std = correlation * new_portfolio_beta  # Simplified
    sharpe_ratio = round((expected_return - risk_free_rate) / portfolio_std, 3) if portfolio_std > 0 else 2.5
    
    return {
        'correlation': correlation,
        'sharpe_ratio': sharpe_ratio,
        'current_esg': current_esg,
        'new_portfolio_esg': new_portfolio_esg,
        'expected_return': expected_return,
        'new_sector': stock_sector
    }

def analyze_portfolio(portfolio, investment_amount):
    """Analyze the portfolio and suggest stocks"""
    print("\n=== ANALYZING PORTFOLIO ===")
    print("Processing your data...")
    
    try:
        # Simulate processing time for better UX
        for i in range(5):
            print("." * (i + 1))
            time.sleep(0.3)
        
        # Select a stock not currently in the portfolio
        current_tickers = list(portfolio.keys())
        suggested_stock = suggest_ticker(current_tickers)
        
        # Calculate portfolio metrics
        metrics = calculate_metrics(portfolio, suggested_stock, investment_amount)
        
        # Get company information
        company_info = get_company_info(suggested_stock)
        stock_details = get_stock_data(suggested_stock)
        
        print("\n=== ANALYSIS RESULTS ===")
        
        # Determine if ESG score is improving or worsening
        esg_change = metrics['new_portfolio_esg'] - metrics['current_esg']
        if abs(esg_change) < 0.1:  # If change is very small, consider it neutral
            esg_status = "neutral"
            esg_symbol = "→"
        elif esg_change < 0:
            esg_status = "improving (lower is better)"
            esg_symbol = "↓"
        else:
            esg_status = "increasing slightly"
            esg_symbol = "↑"
        
        # Format the annual return percentage
        annual_return_pct = f"{metrics['expected_return']*100:.1f}%"
        
        # Get company name and ticker info
        company_name = company_info.get('name', stock_details.get('company_name', suggested_stock))
        
        # Company details section
        company_details = f"We suggest investing in {suggested_stock} - {company_name}\n\n"
        company_details += "COMPANY DETAILS:\n"
        
        # Add industry/sector information
        industry = company_info.get('industry', metrics.get('new_sector', 'General'))
        company_details += f"- Industry: {industry}\n"
        
        # Add description 
        description = company_info.get('description', f"A company in the {industry} sector.")
        if len(description) > 200:  # Truncate very long descriptions
            description = description[:197] + "..."
        company_details += f"- Description: {description}\n"
        
        # Add market cap and stock price if available
        if 'market_cap' in stock_details:
            company_details += f"- Market Cap: {stock_details['market_cap']}\n"
        if 'stock_price' in stock_details:
            company_details += f"- Current Price: {stock_details['stock_price']}\n"
            
        # Add financial performance if available
        if 'performance' in company_info and company_info['performance']:
            company_details += f"- Recent Performance: {company_info['performance']}\n"
        elif 'revenue' in company_info:
            company_details += f"- Revenue: {company_info['revenue']}\n"
            
        # Add other optional details if available
        if 'founded' in company_info and company_info['founded']:
            company_details += f"- Founded: {company_info['founded']}\n"
        if 'headquarters' in company_info and company_info['headquarters']:
            company_details += f"- Headquarters: {company_info['headquarters']}\n"
        
        # Portfolio metrics section
        portfolio_metrics = (
            f"\nPORTFOLIO METRICS AFTER ADDING {suggested_stock}:\n"
            f"- Portfolio correlation: {metrics['correlation']} (lower is better)\n"
            f"- Expected annual return: {annual_return_pct}\n"
            f"- ESG score: {metrics['current_esg']} {esg_symbol} {metrics['new_portfolio_esg']} ({esg_status})\n\n"
            f"This recommendation is based on optimizing your portfolio for:\n"
            f"- Maximum diversification (minimum correlation)\n"
            f"- Strong risk-adjusted returns\n"
            f"- Improved ESG (Environmental, Social, Governance) profile"
        )
        
        # Combine all sections
        result = company_details + portfolio_metrics
        
        print(result)
        
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {e}")
        print(f"\nError analyzing portfolio: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
    
    input("\nPress Enter to continue...")

def show_esg_info(ticker):
    """Show ESG information for a specific stock"""
    print(f"\n=== ESG ANALYSIS FOR {ticker} ===")
    
    try:
        # Get ESG data for the requested ticker
        esg_data = get_esg_scores(ticker)
        total_esg = esg_data.get('total', 0)
        env_score = esg_data.get('environmental', 0)
        social_score = esg_data.get('social', 0)
        gov_score = esg_data.get('governance', 0)
        
        # Get stock data for additional context
        stock_data = get_stock_data(ticker)
        sector = stock_data.get('sector', 'Unknown')
        
        # Determine risk level
        if total_esg <= 15:
            risk_level = "low"
            risk_color = "excellent"
        elif total_esg <= 25:
            risk_level = "medium"
            risk_color = "average"
        else:
            risk_level = "high"
            risk_color = "concerning"
        
        # Identify strongest and weakest ESG components
        scores = [
            ("Environmental", env_score),
            ("Social", social_score),
            ("Governance", gov_score)
        ]
        strongest = min(scores, key=lambda x: x[1])
        weakest = max(scores, key=lambda x: x[1])
        
        # Format the analysis text
        analysis = f"""
A company's total ESG risk score reflects its overall exposure to environmental, social, and governance risks
and how well those risks are managed. A lower score indicates better management of ESG risks.

For {ticker} ({sector}), the total ESG risk score is {total_esg}, which is considered {risk_level} ({risk_color}).

Breaking it down by category:
- Environmental: {env_score} - Impact on natural environment
  (carbon emissions, resource use, waste management, climate initiatives)
  
- Social: {social_score} - Impact on people and communities
  (labor practices, customer relations, community engagement, data privacy)
  
- Governance: {gov_score} - Corporate leadership and oversight
  (board structure, executive compensation, ethical practices, shareholder rights)

{ticker}'s strongest ESG area is {strongest[0]} with a score of {strongest[1]}.
Its most challenging area is {weakest[0]} with a score of {weakest[1]}.

"""
        
        # Add sector comparison if available
        if hasattr(get_esg_scores, "sector_averages") and sector in get_esg_scores.sector_averages:
            sector_avg = get_esg_scores.sector_averages[sector]
            comparison = "better than" if total_esg < sector_avg else "worse than"
            analysis += f"\nCompared to its sector average of {sector_avg}, {ticker} performs {comparison} other {sector} companies."
        
        print(analysis)
            
    except Exception as e:
        logger.error(f"Sorry, no ESG data available for: {e}. Try a different stock.")
    
    input("\nPress Enter to continue...")



def show_main_menu():
    """Display the main menu and get user choice"""
    print_header()
    print("MAIN MENU")
    print("1. Get Portfolio Suggestions")
    print("2. Analyze ESG Scores")
    print("3. Visualize Stock Performance")
    print("4. Exit")
    
    choice = input_with_validation(
        "\nEnter your choice (1-4): ",
        lambda x: x.isdigit() and 1 <= int(x) <= 4,
        "Please enter a number between 1 and 4."
    )
    
    return int(choice)

def get_portfolio_suggestions():
    """Complete workflow for getting portfolio suggestions"""
    print_header()
    portfolio = get_current_portfolio()
    investment_amount = get_additional_investment()
    
    print("\nYour current portfolio:")
    for ticker, amount in portfolio.items():
        print(f"  {ticker}: ${amount:.2f}")
    print(f"Additional investment: ${investment_amount:.2f}")
    
    proceed = input("\nAnalyze this portfolio for suggestions? (y/n): ").lower().strip()
    if proceed == 'y':
        analyze_portfolio(portfolio, investment_amount)

def analyze_esg_scores():
    """Workflow for analyzing ESG scores"""
    print_header()
    
    # Show available tickers
    print("Sample tickers from S&P 500 (you can enter others as well):")
    sample_display = ", ".join(random.sample(SAMPLE_SP500, min(10, len(SAMPLE_SP500))))
    print(f"  {sample_display}, ...")
    
    ticker = input_with_validation(
        "Enter ticker symbol to analyze ESG scores (e.g., AAPL): ",
        lambda x: len(x) > 0 and len(x) <= 5,
        "Please enter a valid ticker symbol (1-5 characters)."
    ).upper()
    
    show_esg_info(ticker)

def visualize_stock_performance():
    """Workflow for visualizing stock performance"""
    clear_screen()
    
    # Show available tickers
    sample_display = ", ".join(random.sample(SAMPLE_SP500, min(10, len(SAMPLE_SP500))))
    print(f"Sample tickers: {sample_display}")
    
    ticker = input_with_validation(
        "Enter ticker symbol to visualize (e.g., AAPL): ",
        lambda x: len(x) > 0 and len(x) <= 5,
        "Please enter a valid ticker symbol (1-5 characters)."
    ).upper()
    
    try:
        # Absolute import 
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "data_visualization", 
            os.path.join(os.path.dirname(__file__), "wealthspread", "data_visualization_historic_performance.py")
        )
        vis_script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vis_script)
        
        # Display stock information
        stock_data = get_stock_data(ticker)
        company_info = get_company_info(ticker)
        esg_data = get_esg_scores(ticker)
        
        # Ensure Visualization Example directory exists
        vis_dir = os.path.join('wealthspread', 'Visualization Example')
        os.makedirs(vis_dir, exist_ok=True)
        
        # Generate visualization
        import matplotlib.pyplot as plt
        plt.switch_backend('TkAgg')  # Try a different backend that works well in terminal
        output_path = None
        
        # Temporarily modify the plot function to return both path and figure
        original_plot_func = vis_script.plot_stock_history
        def modified_plot_history(symbol):
            nonlocal output_path
            output_path = original_plot_func(symbol)
            return output_path
        
        vis_script.plot_stock_history = modified_plot_history
        
        # Generate the plot
        vis_script.plot_stock_history(ticker)
        
        # Print key information
        print(f"\n{ticker} Stock Overview:")
        print(f"Company: {stock_data.get('company_name', 'N/A')}")
        print(f"Market Cap: {stock_data.get('market_cap', 'N/A')}")
        print(f"Current Price: {stock_data.get('stock_price', 'N/A')}")
        
        # ESG Metrics
        print("\nESG Metrics:")
        print(f"Total Score: {esg_data.get('total', 'N/A')}")
        print(f"Environmental: {esg_data.get('environmental', 'N/A')}")
        print(f"Social: {esg_data.get('social', 'N/A')}")
        print(f"Governance: {esg_data.get('governance', 'N/A')}")
        
        # Show the plot
        plt.show()
    
    except Exception as e:
        print(f"\nError generating visualization: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point for the interactive CLI"""
    try:
        while True:
            choice = show_main_menu()
            
            if choice == 1:
                get_portfolio_suggestions()
            elif choice == 2:
                analyze_esg_scores()
            elif choice == 3:
                visualize_stock_performance()
            elif choice == 4:
                print("\nThank you for using Wealth Spread! Goodbye.")
                break
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check the log file for details.")

if __name__ == "__main__":
    main()
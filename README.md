# Wealth Spread: Intelligent Portfolio Diversification Tool

## Team Members

- Raabiyal Ishaq <rishaq@uchicago.edu>
- Marie Farhat <mariefarhat@uchicago.edu>
- Khushi Desai <khushi@uchicago.edu>
- Shumaila Abbasi <shumaila@uchicago.edu>

## Abstract

Wealth Spread is an innovative Portfolio Optimization & Diversification Tool designed to revolutionize how individual investors approach stock portfolio management. In today's complex financial landscape, individual investors often struggle to effectively diversify their investments, leading to unnecessary risk and potential financial volatility. 

Our tool addresses this challenge by providing a comprehensive, data-driven approach to portfolio optimization. By leveraging advanced data analysis techniques, including correlation analysis, historical price tracking, and ESG (Environmental, Social, and Governance) scoring, the tool provides users with actionable insights to minimize portfolio risk while maximizing potential returns.

## Project Motivation

Investment diversification is more than just spreading money across different stocks. It requires a nuanced understanding of how different assets interact, their historical performance, and their potential future behavior. Traditional investment approaches often rely on intuition or limited information, which can lead to suboptimal investment decisions. 

Wealth Spread leverages cutting-edge data science techniques to provide a more intelligent, data-driven approach to portfolio management. We go beyond simple diversification by incorporating multiple layers of analysis, examining the complex relationships between different stocks, their correlation patterns, and their broader economic and sustainability contexts.

# Link to the Tutorial Video 
https://drive.google.com/file/d/1YP4KzmAb3Z7C1LID5qGs4gi6z533cbW1/view?usp=sharing

## How to Run

### Prerequisites

- Python 3.8 or higher
- `uv` package manager

### How to Run

**Quickstart Guide**
- uv sync
- uv run wealthspread_cli.py

#### Detailed How to Run the Project
**Step 0: Run uv sync**
- With the repository open, run the 'uv sync' command in the terminal

**Step 1: Engage the Command Line Application**
- In the terminal, enter command 'uv run wealthspread_cli.py'
- You should see the main application menu titled "Wealthspread"
- A menu of 3 selection options will appear

**Step 2: Analyze Portfolio & Get Stock Suggestions**
- In the command line, type '1' and hit enter
- You will be prompted to enter the number of stocks in your portfolio (between 1 and 5). Enter a valid number.
- For each stock in your portfolio, you will be asked to:
    - First enter the ticker symbol (e.g. 'AAPL')
    - Second enter the dollar amount (e.g. '1000')
- Next, you will be prompted to enter the dollar amount you wish to invest today. Enter a numerical value (e.g. '200')
- Finally, when ready to execute the portfolio analysis, enter 'y' into the command line
- View your custom portfolio analysis and stock suggestion!
- Follow the instructions to return to the main menu by hitting 'enter' on your keyboard

**Step 3: Get ESG Information for a Ticker**
- In the command line, type '2' and hit enter
- Enter a single stock ticker (e.g. 'AAPL') in the command line
- The wealthspread application will output the ESG risk score breakdown for your selected stock
- Follow the instructions to return to the main menu by hitting 'enter' on your keyboard

**Step 4: Exit the Application**
- In the command line, type '3' to exit the application
- You may revisit Step 1 to re-engage with Wealthspread

**Optional: Refresh Scraped Data**
- The S&P500 is rebalanced quarterly, typically on the 3rd Friday of March, June, September, and December.
- To get the latest list of S&P500 stocks, run the following commands from the terminal:
    - 'uv run wealthspread/scrape/stockanalysis_scrape.py'
    - Validate the scraped results in wealthspread/scrape/SA_sp500_tickers.json
- Next, update each stock's company data by running the following command:
    - 'uv run wealthspread/scrape/companyinfo_scrape.py'
    - Validate the scraped results in wealthspread/scrape/company_info.json

**Optional: Refresh Stock Data**
- To update Stock data, need to run the following:
- twelvedata_api.fetch_and_cache() from the correlations folder
- Use API_KEY sent on email in twelvedata_api.py

### How to Run Tests
'pytest tests/esg_tests.py'
'pytest tests/scraping_tests.py'


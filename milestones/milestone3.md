# Milestone #3: Project Prototype & Check-in

## Core Implementation Details

Our Portfolio Diversification Tool currently consists of **four** completed Python programs and one planned program for data collection, analysis, and visualization.

The data collection system has been built with comprehensive functionality for gathering S&P 500 company information. We have created a web scraping system that collects data from multiple sources, ensuring data accuracy and completeness. The TwelveData API integration has been implemented with an efficient caching system that properly manages rate limits of 800 calls per day and 8 calls per minute. This system successfully retrieves and stores 5-year historical price data for all S&P 500 companies. Additionally, we are in the process of implementing ESG data collection, providing sustainability metrics for portfolio analysis.

### 1. Web Scraping Implementations

**`stockanalysis_scrape.py`**
This program scrapes detailed S&P 500 company information from StockAnalysis.com. It implements:
- Rate-limited web requests (0.1-second delay between requests)
- Domain verification for security
- Structured data collection for each company including:
  - Ticker symbols
  - Company names
  - Market capitalization
  - Current stock prices
  - Percentage changes
  - Revenue data
  - Company-specific webpage links
The data is saved in JSON format as "SA_sp500_tickers.json" for easy access and integration.

**`companyinfo_scrape.py`**
This program takes the company page url from "SA_sp500_tickers.json" and scrapes 
further company information from StockAnalysis.com. It implements:
- Unique key matching based on the ticker symbol (e.g. "AAPL" or "GOOG") from one scraped source
  to scrape from another webpage
- Structured webscraped data collection for each company including:
  - Company background information (industry, employees, etc.)
  - Company financial performance (e.g. annual revenue and YoY change)
- Error handling if no primary key match is found
The data is saved in JSON format as "companyinfo_scrape.json" for easy access and integration.

**`WIP ESG SCRAPING IMPLEMENTATION USING SELENIUM`**
**`MSCI_search.py and SP_Global_search.py`**
These scripts use the selenium library to interact with searchbar functions on the following webpages:
- SP Global: https://www.spglobal.com/esg/solutions/esg-scores-data
- MSCI: https://www.msci.com/our-solutions/esg-investing/esg-ratings-climate-search-tool
The aim of this scraping is to gather ESG (Environmental, Social and Governance) reviews
for a specific ticker symbol in the S&P500 (e.g. 'AAPL') and share the findings as part
of the portfolio optimization result and rationale to help inform our investor (user) on 
the impact of their investment. The intended implementation will:
- Use selenium webdriver capabilities to interact with website search bars
- Pull a unique ticker (matched with the unique IDs from previous webscrapes / portfolio optimization result) and
  input the resulting value into the search box
- Navigate to a new webpage as a result of the search
- Scrape ESG-related data, which will be shared as part of the data visualization.
Currently, both scripts are running into issues caused by bot-detection or cookie interference.
Alternate data sources are being explored to mitigate.

**`ARCHIVED SCRAPING IMPLEMENTATION`**
**`wiki_sp500_list_scrape.py`**
This script collects complementary S&P 500 data from Wikipedia, featuring:
- The same secure request handling system
- Collection of different data points:
  - Stock symbols
  - Exchange URLs
  - Security names
  - Wikipedia page links
The data is stored in "Wiki_sp500_tickers.json", providing additional context and verification for our company list.

### 2. Use of TwelveData API  
**`correlation/correlation.py`**
The correlation.py file implements the core functionality for handling stock market data through the TwelveData API. Here's a concise summary:
Key Functions:

1. `tickers_list_creator()`: Creates a list of S&P 500 tickers from previously scraped data in "SA_sp500_tickers.json"

2. `calculate_weight_of_portfolio()`: Calculates normalized weights for stocks in a portfolio based on investment amounts

3. `url_to_cache_key()`: Converts API URLs to safe cache keys by sanitizing characters and ensuring proper formatting

4. `fetch_and_cache()`: Main API handling function that:
    - Implements rate limiting (10-second delay between calls)
    - Checks cache before making new API calls
    - Fetches 5-year historical data for each stock
    - Stores responses in "_cache2" directory
    - Creates "company_info.json" with processed data

5. `parse_csv_to_dict()`: Converts CSV responses from the API into dictionaries with dates and closing prices

The file establishes a robust system for data retrieval and caching, ensuring efficient use of the TwelveData API while maintaining a comprehensive database of historical stock prices for analysis.

This mathematical analysis module (`correlation.py`) implements the core portfolio optimization logic. Here's a concise summary:

### 3. Mathematical Implementation: Portfolio Optimization Through Correlation Analysis
**`correlation/simulation.py`**
**Key Functions:**
1. `calculate_weight_of_portfolio()`: Normalizes portfolio weights based on investment amounts (e.g., {'GOOG': 10000, 'AAPL': 20000} → percentage weights)

2. `convert_to_percentchange()`: 
   - Reads historical price data from "company_info.json"
   - Calculates percentage changes for each stock
   - Stores results in "percent_changes.json"

3. `weighted_mean_correlation()`: 
   - Takes correlation matrix and portfolio weights
   - Uses NumPy for matrix operations
   - Calculates weighted correlation for portfolio diversification

4. `correlation_matrix()`:
   - Creates correlation matrix from percentage changes
   - Saves to "correlation_matrix.csv"

5. `suggest_stocks()`: Core optimization function that:
   - Takes current portfolio and new investment amount
   - Analyzes possible stock combinations
   - Uses correlation minimization to find best diversification
   - Returns optimal stock suggestion and correlation score

The module focuses on portfolio optimization through correlation analysis, helping users maximize diversification by suggesting stocks that minimize portfolio correlation.

Would you like me to explain any specific function or the mathematical methodology in more detail?

### 4. Visualization System (to be integrated with the UI)

**`data_visualization_historic_performance.py`**
Our visualization program creates professional-grade stock performance charts using matplotlib. Key features include:
- Historical price visualization with closing prices
- Price range display using shaded areas
- Statistical overlay showing:
  - Current price
  - 5-year high/low values
  - Average price calculations
- Professional styling elements:
  - Clear gridlines
  - Rotated date labels
  - Statistical information box
- High-resolution output (300 DPI) saved as PNG files

This will be integrated into the UI, this is just the prototype with singular example usage, the sample PNGs have been uploaded on the repository.

### In Progress
The user interface development is currently our primary focus. We are working on creating an intuitive interface that will allow users to easily select companies, input their investment amounts, and view portfolio analysis results. The interface will incorporate our visualization components and provide a comprehensive dashboard for portfolio analysis. This development includes creating efficient company selection mechanisms and investment input systems that will integrate seamlessly with our existing data processing pipeline.

We are also in the process of integrating all components into a unified system and cleaning the code. This involves merging our separate modules while maintaining code efficiency and reliability. Our team is focused on optimizing the codebase, improving error handling mechanisms, and ensuring comprehensive documentation throughout the system.


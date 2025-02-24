# Milestone #3: Project Prototype & Check-in

## Core Implementation Details

Our Portfolio Diversification Tool currently consists of **four** completed Python programs and one planned program for data collection, analysis, and visualization.

The data collection system has been built with comprehensive functionality for gathering S&P 500 company information. We have created a web scraping system that collects data from multiple sources, ensuring data accuracy and completeness. The TwelveData API integration has been implemented with an efficient caching system that properly manages rate limits of 800 calls per day and 8 calls per minute. This system successfully retrieves and stores 5-year historical price data for all S&P 500 companies. Additionally, we have implemented ESG data collection, providing sustainability metrics for portfolio analysis.

WRITE ABOUT THE CORRELATION UNDERSTANDING - Raabi

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

**`wiki_sp500_list_scrape.py`**
This script collects complementary S&P 500 data from Wikipedia, featuring:
- The same secure request handling system
- Collection of different data points:
  - Stock symbols
  - Exchange URLs
  - Security names
  - Wikipedia page links
The data is stored in "Wiki_sp500_tickers.json", providing additional context and verification for our company list.

### 2. Visualization System

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

### 3. Using TwelveDataAPI to get 5 years of stock data 

**`xyz.py`** (TO BE COMPLETED BY RAABIYAL)



### In Progress
The user interface development is currently our primary focus. We are working on creating an intuitive interface that will allow users to easily select companies, input their investment amounts, and view portfolio analysis results. The interface will incorporate our visualization components and provide a comprehensive dashboard for portfolio analysis. This development includes creating efficient company selection mechanisms and investment input systems that will integrate seamlessly with our existing data processing pipeline.

We are also in the process of integrating all components into a unified system and cleaning the code. This involves merging our separate modules while maintaining code efficiency and reliability. Our team is focused on optimizing the codebase, improving error handling mechanisms, and ensuring comprehensive documentation throughout the system.
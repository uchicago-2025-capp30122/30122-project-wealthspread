# Wealth Spread

## Abstract

We are creating a Portfolio Diversification Tool focused on S&P 500 companies that enables users to optimize their stock portfolios for maximum diversification and reduced risk. The tool allows users to input their current investments by selecting specific S&P 500 companies and their corresponding investment amounts [e.g., AAPL (Apple): $500, TSLA (Tesla): $300, CVS (CVS Pharmacy): $200]. Using 5-year historical data, the system analyzes stock correlations and returns to provide insights on portfolio diversification. The tool highlights potential concentration risks in the user's portfolio and suggests optimization strategies. Additionally, it incorporates ESG (Environmental, Social, and Governance) scores of S&P 500 companies, helping users understand and potentially improve the sustainability profile of their investments while maintaining their diversification goals.

## Data Sources

### Data Reconciliation Plan

All datasets will be linked using stock ticker symbols (e.g., AAPL, TSLA) as the primary unique key. The S&P 500 components list will serve as our base dataset, with historical price data from TwelveData and ESG scores from SPGlobal being mapped to these tickers. All data processing will maintain consistent ticker symbol formatting for accurate joining.

## Mathematical Framework and Implementation
Our analysis will utilize NumPy and Pandas libraries for data manipulation and statistical calculations:
# Data Processing
- Convert API data into Pandas DataFrames for efficient manipulation
- Clean and preprocess data to handle missing values and outliers
- Standardize date formats and align time series data
# Portfolio Analysis
- Calculate portfolio weights based on user investment amounts
- Compute daily returns from historical price data
- Generate correlation matrix to understand relationships between stocks
# Risk Assessment
- Calculate portfolio variance and volatility metrics
- Analyze portfolio concentration and diversification levels
- Evaluate sector-based risk exposure
# Optimization Strategy
- Use correlation analysis to identify concentration risks
- Apply portfolio optimization techniques to suggest improved distributions

### Data Source #1: S&P 500 Index Components
Data Type: Bulk data from Wikipedia/official S&P website

Challenges:
- Need to handle periodic updates to S&P 500 composition
- Some companies have multiple share classes listed

Records: ~505 records (including companies with multiple share classes)
Properties: 4 columns (Symbol, Company Name, Sector, Industry)
Exploration Notes: The list requires monthly validation as companies can be added/removed from the index. Companies with multiple share classes (like GOOGL/GOOG) need special handling to avoid duplication in analysis.

### Data Source #2: TwelveData API - Historical Stock Data

Data Type: REST API (supports both .csv and JSON format extraction)

Challenges:
- Limited to 800 API calls per user and 8 calls per minute
- Need to implement robust caching system to maximize API usage efficiency
- Need to handle cases where cache needs updating
- Need to implement proper error handling for API timeouts/failures
- Large data volume when fetching 5 years of daily data for all S&P 500 stocks

Here's an example of an output:
{
	"meta": {
		"symbol": "AAPL",
		"interval": "1min",
		"currency": "USD",
		"exchange_timezone": "America/New_York",
		"exchange": "NASDAQ",
		"mic_code": "XNGS",
		"type": "Common Stock"
	},
	"values": [
		{
            "datetime": "2025-01-31 15:59:00",
			"open": "235.77000",
			"high": "236.080002",
			"low": "235.75",
			"close": "235.86000",
			"volume": "1214983"
		},
		{
			"datetime": "2025-01-31 15:58:00",
			"open": "235.91000",
			"high": "235.98000",
			"low": "235.64000",
			"close": "235.77000",
			"volume": "561576"
		}]
}

Exploration Notes: Initial API testing shows reliable data availability for the requested 5-year period. The API returns well-structured JSON data that requires minimal cleaning. Given the API limitations (800 calls per user, 8 per minute), we will implement a caching system to store historical data locally. The cache will be updated periodically to maintain data freshness while staying within API limits. New user queries will first check the cache before making API calls, significantly reducing the number of API requests needed.

### Data Source #3: SPGlobal.com ESG Scores

Data Type: Web scraping
Challenges:
- Web scraping requires robust error handling and rate limiting
- Website structure changes could break the scraper
- Need to handle authentication/sessions if required
- Potential anti-scraping measures need to be addressed

Records: ~500 records (current S&P 500 companies)
Properties: Expected columns include Company Symbol and ESG Score (exact structure to be determined after initial scraping)
Exploration Notes: Will need to implement appropriate delays between requests to avoid overwhelming the server. Regular validation of scraped data quality is necessary. May need to implement proxy rotation or other techniques to ensure reliable data collection.

## Project Plan

# Required Components
1. Data Collection and Storage System (Primary: Marie Farhat)
- TwelveData API Integration with caching (800 calls limit, 8 per minute)
- S&P 500 Components Data Collection
- SPGlobal ESG Data Web Scraping
- Database Setup for Data Storage

2. Data Processing and Cleaning (Primary: Shumaila Abbasi)
- Handling Missing Values (if any)
- Time Series Alignment
- Data Format Consistency
- Integration of Multiple Data Sources

3. Mathematical Implementation (Primary: Raabiyal Ishaq)
- Correlation Analysis Implementation
- Portfolio Risk Assessment
- Diversification Metrics
- Statistical Analysis Framework
- Optimization Algorithms

4. User Interface Development (Primary: Khushi Desai)
- Company Selection Interface
- Investment Input System
- Portfolio Analysis Dashboard
- Visualization Components
- Risk and ESG Score Display

# Tentative Timeline
Milestone #3 - Week 7 (Feb 19-25)
Target: Functional Prototype
- Marie: Complete API integration and basic web scraping
- Shumaila: Have basic data cleaning pipeline operational
- Raabiyal: Implement initial correlation and risk analysis
- Khushi: Develop basic UI with company selection and investment input
- All: Integration testing of basic functionality

Weeks 8-9 (Feb 26-Mar 8)
Week 8:
- Marie: Optimize data collection, implement full caching system
- Shumaila: Enhance data cleaning, implement validation checks
- Raabiyal: Complete portfolio optimization algorithms
- Khushi: Add advanced visualizations and dashboard components

Week 9:
- Marie & Shumaila: Final data pipeline optimization
- Raabiyal & Khushi: UI/UX refinements
- All: System integration and testing
- March 8: Internal project freeze for testing

Project Fair - Week 10 (March 10)
- March 9: Final testing and preparation for demo
- March 10: Project Fair Presentation
- March 11: Final documentation and code cleanup
- Final Deadline: March 11th 11:59pm

Cross-Team Collaboration
- Daily standup meetings during final weeks
- Collaborative testing sessions
- Documentation responsibilities shared across team
- Regular code reviews and merges

## Questions


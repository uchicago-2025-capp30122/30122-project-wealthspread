# Project Paper

# Link to the Tutorial Video 
https://drive.google.com/file/d/1YP4KzmAb3Z7C1LID5qGs4gi6z533cbW1/view?usp=sharing

## WealthSpread Team Members:
- Raabiyaal Ishaq - rishaq@uchicago.edu
- Marie Farhat - mariefarhat@uchicago.edu
- Shumaila Abbasi - shumaila@uchicago.edu
- Khushi Desai - khushi@uchicago.edu

## Project Abstract:
This project implements a comprehensive investment portfolio analysis and recommendation system called WealthSpread. The application assists users in making informed investment decisions by analyzing financial metrics, ESG (Environmental, Social, and Governance) scores, and historical stock performance data. WealthSpread combines traditional financial mathematics with modern ESG considerations to provide users with balanced investment recommendations that align with both financial goals and sustainability concerns. The system analyzes correlation matrices, calculates Sharpe ratios, and runs simulations to recommend optimal stock combinations from the S&P 500 index.

## Data Sources

### S&P 500 Index Components

The S&P 500 serves as the foundational dataset for our project.
This comprehensive index represents 500 of the largest publicly traded companies in the United States,
providing a robust and representative sample of the corporate landscape. 

**How to Obtain**: 
- Freely available from the Stock Analysis website
- Requires monthly validation due to index composition changes
- Link : https://stockanalysis.com/list/sp-500-stocks/
- This data source is webscraped for our project

### Historical Stock Data (TwelveData API)

**API Details**:
- Register at: https://twelvedata.com/pricing
- Free version: 800 API calls per day
- Limitations: 8 calls per minute

We've implemented a caching system that efficiently manages API call limitations,
storing and updating data to minimize unnecessary API requests. 
The system retrieves comprehensive 5-year historical price data for S&P 500 companies.

### ESG Score Integration

**Data Collection**:
- Source: From Yahoo Finance (https://finance.yahoo.com/); API via yfinance library (https://pypi.org/project/yfinance/)
- Method: Collecting Environmental, Social, and Governance (ESG) risk ratings
- Yahoo Finance sources its risk ratings from Sustainalytics, a Morningstar company

## Limitations and Considerations

- The tool provides data-driven insights but does not constitute financial advice
- Investment decisions should consider individual financial situations
- Recommended to consult with financial professionals
- Data sources may have intermittent availability


## Overall Structure of the Project:
The project is structured into several main components:

1. *Data Collection*: This component handles the acquisition of stock data, ESG scores, and S&P 500 tickers through:
  - API integration with TwelveData for historical stock price data
  - Web scraping of ESG scores and sustainability metrics
  - Web scraping of S&P 500 stock information from Wikipedia
 
2. *Financial Analysis*: This core component provides the mathematical foundation for:
  - Calculation of Sharpe ratios for risk-adjusted return assessment
  - Generation of correlation matrices to analyze relationships between stocks
  - Portfolio simulation and optimization algorithms
  - Risk assessment and diversification analysis
 
3. *ESG Analysis*: This component processes and integrates sustainability metrics into the investment decision process:
  - ESG score normalization and weighting
  - Integration of ESG factors with financial performance data
  - Sustainability-focused portfolio recommendations
 
4. *User Interface*: A command-line application that:
  - Guides users through the portfolio analysis process
  - Provides an intuitive interface for interacting with complex financial data
 
5. *Testing and Documentation*: Includes test suites and documentation:
  - Unit tests for individual components
  - Integration tests for system functionality
  - User documentation and examples


## Responsibilities of each member:


### Raabiyaal
*Role*: Financial Mathematics & Portfolio Analysis
- Developed the core financial mathematics engine for portfolio analysis
- Implemented the portfolio.py and simulation.py to calculate Sharpe ratios for risk-adjusted return measurement
- Created correlation matrix generation functionality to analyze stock relationships

### Marie
*Role*: ESG Analysis & Data Collection
- Web scraped ESG scores from sustainability reporting sources
- Web scraped S&P 500 stock tickers and related information from Wikipedia
- Implemented data cleaning and normalization processes for ESG metrics

### Shumaila
*Role*: API Integration & Stock Data Collection
- Implemented TwelveData API integration to acquire 5 years of historical stock data
- Web scraped additional company information to supplement API data
- Created data validation and error handling for API connections


### Khushi
*Role*: User Interface & Project Presentation
- Designed and built the entire command-line application interface
- Created the UI/UX flow for user interaction with the system
- Developed the project logo and branding elements

### Team Collaboration
- All team members participated in regular debugging sessions
- Each member wrote tests
- Collaborative repository organization and code structure planning
- Regular meetings for brainstorming and feedback
- Cross-functional support throughout development
- Collaborated on producing the tutorial video


## Conclusion

The WealthSpread project successfully combines traditional financial analysis techniques with modern ESG considerations to provide users with a comprehensive investment recommendation tool. The application demonstrates the potential for integrating sustainability metrics into investment decision processes without sacrificing financial performance.


The team effectively utilized web scraping, API integration, and financial mathematics to create a cohesive system that provides valuable insights for investors. The command-line interface makes complex financial analysis accessible to users without requiring advanced financial knowledge.


Future enhancements could include:
- Development of a robust website interface to make the tool more accessible to a wider audience
- Expansion of the analysis to include more market indices beyond the S&P 500
- Development of a graphical user interface for improved visualization
- Implementation of machine learning algorithms for predictive analysis
- Integration with brokerage APIs for real-time portfolio management
- Incorporation of additional alternative data sources for more comprehensive analysis


WealthSpread represents an important step toward democratizing sophisticated investment analysis while promoting responsible investment principles through ESG integration.

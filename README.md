# Wealth Spread: Intelligent Portfolio Diversification Tool

## Team Members

- Raabiyal Ishaq <rishaq@uchicago.edu>
- Marie Farhat <mariefarhat@uchicago.edu>
- Khushi Desai <khushi@uchicago.edu>
- Shumaila Abbasi <shumaila@uchicago.edu>

## Abstract

Wealth Spread is an innovative Portfolio Diversification Tool designed to revolutionize how individual investors approach stock portfolio management. In today's complex financial landscape, individual investors often struggle to effectively diversify their investments, leading to unnecessary risk and potential financial volatility. 

Our tool addresses this challenge by providing a comprehensive, data-driven approach to portfolio optimization. By leveraging advanced data analysis techniques, including correlation analysis, historical price tracking, and ESG (Environmental, Social, and Governance) scoring, the tool provides users with actionable insights to minimize portfolio risk while maximizing potential returns.

## Project Motivation

Investment diversification is more than just spreading money across different stocks. It requires a nuanced understanding of how different assets interact, their historical performance, and their potential future behavior. Traditional investment approaches often rely on intuition or limited information, which can lead to suboptimal investment decisions. 

Wealth Spread leverages cutting-edge data science techniques to provide a more intelligent, data-driven approach to portfolio management. We go beyond simple diversification by incorporating multiple layers of analysis, examining the complex relationships between different stocks, their correlation patterns, and their broader economic and sustainability contexts.

## Data Sources

### S&P 500 Index Components

The S&P 500 serves as the foundational dataset for our project. This comprehensive index represents 500 of the largest publicly traded companies in the United States, providing a robust and representative sample of the corporate landscape. 

**How to Obtain**: 
- Freely available from Wikipedia or official S&P website
- Requires monthly validation due to index composition changes

### Historical Stock Data (TwelveData API)

**API Details**:
- Register at: https://twelvedata.com/pricing
- Free version: 800 API calls per day
- Limitations: 8 calls per minute

We've implemented a caching system that efficiently manages API call limitations, storing and updating data to minimize unnecessary API requests. The system retrieves comprehensive 5-year historical price data for S&P 500 companies.

### ESG Score Integration

**Data Collection**:
- Source: Web scraping from SPGlobal.com
- Method: Collecting Environmental, Social, and Governance (ESG) ratings
- Current Status: Implemented via web scraping
- Challenges: Requires robust error handling and potential alternative sources

## How to Run

### Prerequisites

- Python 3.8 or higher
- `uv` package manager

### Project Setup

**Step 1: Run Data Scrapers**
( WRITE AFTER UNDERSTANDING UV )

## Limitations and Considerations

- The tool provides data-driven insights but does not constitute financial advice
- Investment decisions should consider individual financial situations
- Recommended to consult with financial professionals
- Data sources may have intermittent availability

## Future Development

- Continuous improvement of data sources
- Refinement of correlation analysis algorithms
- Expansion of user interface
- Goal: Make sophisticated investment analysis accessible to everyone



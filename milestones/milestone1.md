# {Team Name}

## Members

- Raabiyaal Ishaq <rishaq@uchicago.edu>
- Marie Farhat <mariefarhat@uchicago.edu>
- Khushi Desai <khushi@uchicago.edu>
- Shumaila Abbasi <shumaila@uchicago.edu>


## Abstract

Creating a Portfolio Diversification Tool which will allow users to optimize 
their investment portfolios for maximum diversification and reduced risk. 
The tool would use historical data on asset classes such as stocks, bonds,
 commodities, and cryptocurrencies to calculate correlations between investments.
  Users can add data of their current investments, and the platform would
   suggest which assets (stocks, bonds, commodities, cryptocurrencies) 
   they should invest in to maximize diversification. It will also
    highlight assets that would increase concentration risk. Additionally, 
    we can request investor attributes (age, financial literacy, risk 
    preference,     risk tolerance) and suggest assets based on that as well.
     Moreover, 
    we can include other factors such as ESG score to give a rating of 
    their current portfolio and suggest stocks to improve their portfolio
     ESG score.

## Preliminary Data Sources

For each source please add a section with the following:

### Data Source #1: {Name}

We have multiple options where we can extract the same data using APIs with 
some limitations in each. Mentioned below are 4.

### Data Source #1: Bloomberg Terminal
- The Bloomberg Terminal is accessible through the Booth School of Business 
Computer Lab, which can be accessed using our university accounts. However, 
there is no direct link available for remote access.
- Data can be extracted manually in CSV format, one dataset at a time, 
directly from the Bloomberg Terminal. Alternatively, the Bloomberg API
 can be used to automate data extraction.
- Using the Bloomberg API may pose a challenge because the Terminal is 
only available on a specific lab PC, not on our personal computers. If the
 Bloomberg API library is not already installed on these lab PCs, we may need 
 to request IT support to install it.

### Data Source #2: Twelve Data 
- https://twelvedata.com/pricing
- API
- 800 API calls/ day (free version)

### Data Source #3: finnhub 
- https://finnhub.io/pricing
- API
- 60 API calls/ minute (free version)

### Data Source #3: Nasdaq Data Link
- https://docs.data.nasdaq.com/v1.0/docs/getting-started
- API
- 50000 API calls/ day but does not contain all the data that we require.


## Preliminary Project Plan

1.	Identify investment types with readily available data and thoroughly explore
 the data sources mentioned above.
2.	Collect historical price data for these investments over a specific period
 and, where applicable, gather ESG scores for the selected investments.
3.	At this stage, we might not need to calculate the correlation for each asset
 individually. Instead, we can focus on developing a system that calculates 
 the overall correlation of the current assets and simulates the addition of 
 every available investment option. The system would then identify and recommend
  the investment option that maximally decreases the overall correlation.
4.	Create a user interface where the customer has an interactive list view to 
select the investments and an interface where the platform gives its suggestions
 with charts, expected rate of return and other factors.
5.	(Tentative) An addition of ESG (Environment Sustainability & Governance)
 score for each investment may also be added and the user will have an option
  where they can see their current investments’ ESG score and investment 
  suggestions to improve it.
6.	(Tentative) Another addition of returns based on the risk profile of the 
user can be included. User will add their personal details such as age, 
financial literacy, risk aversion, etc. and platform will recommend best 
investment based on risk/return.


## Questions

A **numbered** list of questions for us to respond to.


1. In the professor’s / TA team’s experience, what issues could the API call 
limitations cause for us?
2. Since we have a number of potential data sources to choose from, 
what features should we specifically look out for to make our project
 run more smoothly?

import json

with open('ESG_Scores.json', 'r') as file:
    esg_data = json.load(file)

with open('../scrape/SA_sp500_tickers.json', 'r') as file:
    ticker_data = json.load(file)

def risk_ranking(score):
    if score <= 10:
        return 'low'
    elif 10 < score <= 20:
        return 'medium'
    else:
        return 'high'
    
def generate_esg_analysis(ticker, esg_data):
    company_name = ticker_data[ticker]["company_name"]
    
    if isinstance(esg_data[ticker], str):
        return f"There is no ESG data available for {company_name}."

    esg = esg_data[ticker]['totalEsg']
    e = esg_data[ticker]['environmentScore']
    s = esg_data[ticker]['socialScore']
    g = esg_data[ticker]['governanceScore']
    
    rank = risk_ranking(esg)

    esg_analysis = f"""
    A company's total ESG risk score reflects its overall exposure to environmental, social, and governance risks
    and how well those risks are managed. A lower score indicates better management of ESG risks.
    
    For {company_name}, the total ESG risk score is {esg}, which is considered {rank}. 
    Breaking it down by category:
    - The 'Environmental' risk score is {e}, reflecting the company's environmental impact 
        (carbon emissions, waste management, resource use)
    - The 'Social' risk score is {s}, reflecting the company's social practices
        (labor relations, community engagement, customer satisfaction)
    - The 'Governance' risk score is {g}, reflecting the company's governance structure
        (executive compensation, shareholder rights, business ethics)
    """
    
    return esg_analysis

analysis_dict = {}
for ticker, data in esg_data.items():
    analysis_dict[ticker] = generate_esg_analysis(ticker, esg_data)

with open("ESG_Analysis.json", "w") as file:
    json.dump(analysis_dict, file, indent=2)


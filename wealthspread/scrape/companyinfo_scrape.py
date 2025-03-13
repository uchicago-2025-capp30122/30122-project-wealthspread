import httpx
import lxml.html
import json
from time import sleep

def company_info():
    """
    Fetches and extracts company information and financial performance
    from StockAnalysis.

    Inputs    

    Returns:
            - about_company (str): A brief description of the company.
            - fin_performance (str): The financial performance summary.
                """

# Initialize a dictionary to store the results
company_data = {}

# Counter for skipped companies
skipped_count = 0  
skipped_companies = []  # List to store names of skipped companies

# Create a client with an increased timeout globally
client = httpx.Client(timeout=httpx.Timeout(30))  # Timeout set to 30 seconds

# Open the JSON file containing S&P 500 tickers
with open("wealthspread/scrape/SA_sp500_tickers.json", "r") as file:
    data = json.load(file)  # Load JSON data into a Python dictionary

    for company_name, info in data.items():
        retries = 3  # Retry 3 times
        for attempt in range(retries):
            try:
                # Fetch the webpage using the client with the longer timeout
                response = client.get(info['webpage'])  # No timeout argument needed now
                response.raise_for_status()  # Check if request was successful

                # Parse the HTML response
                parsed_response = lxml.html.fromstring(response.text)

                # Extract company description
                about_elements = parsed_response.xpath('//*[@class="px-0.5 lg:px-0"]')
                about_company = about_elements[0].text_content().strip() if about_elements else "Company description not available."

                # Extract financial performance
                fin_elements = parsed_response.xpath('//*[@class="mb-3"]')
                fin_performance = fin_elements[0].text_content().strip() if fin_elements else "Financial performance data not available."

                # Add the data to the dictionary with the company ticker as the key
                company_data[company_name] = {
                    "about_company": about_company,
                    "fin_performance": fin_performance
                }

                # Break the retry loop if successful
                break  

            except (httpx.RequestError, IndexError, Exception) as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt+1} failed for {company_name}. Retrying...")
                    sleep(2)  # Wait for 2 seconds before retrying
                else:
                    skipped_count += 1
                    skipped_companies.append(company_name)  # Store the skipped company name
                    print(f"Skipping {company_name} due to error: {e}")
                    break

# Print the total number of skipped companies
print(f"\nTotal companies skipped due to errors: {skipped_count}")

# Print the list of skipped companies
if skipped_companies:
    print("Skipped Companies:", ", ".join(skipped_companies))

# Save the company data to a JSON file
with open("wealthspread/scrape/company_info.json", "w") as output_file:
    json.dump(company_data, output_file, indent=4)

print("Company information saved to 'company_info.json'.")

def retreive_company_info(company_name):
    "To retreive already scraped company information"
    
    with open('wealthspread/scrape/company_info.json', 'r') as f:
        data = json.load(f)
        for ticker, info in data.items():
          #  print(ticker, info)
            if ticker == company_name:
                return data[company_name]['about_company'], data[company_name]['fin_performance'] 
       
        

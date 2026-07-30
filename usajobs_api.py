import requests
from utils.config import USAJOBS_API_KEY

def fetch_usajobs(keyword, location="remote", results_per_page=5):

    # define header
    custom_header = {
        "Host": 'data.usajobs.gov',
        'User-Agent': 'jetchaijiajie@gmail.com', 
        "Authorization-Key": USAJOBS_API_KEY 
    }

    # define params
    query_params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPahe": results_per_page
    }

    # construct api
    url = f"https://data.usajobs.gov/api/Search?Keyword={keyword}&LocationName={location}&ResultsPerPage={results_per_page}" 

    # post GET request
    response = requests.get(url, headers=custom_header)
    
    if response.status_code == 200:
        return response.json().get("SearchResult", {}).get("SearchResultItems", [])
    else:
        return []

if __name__ == "__main__":
    jobs = fetch_usajobs("business analyst", location="New York", results_per_page=10)

    for job in jobs:
        title = job['MatchedObjectDescriptor']['PositionTitle']
        agency = job['MatchedObjectDescriptor']['OrganizationName']
        print(f"{title} at {agency}")
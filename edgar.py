from sec_api.index import QueryApi
from dotenv import load_dotenv
import os
import requests




def find_filing(ticker):
    print("ticker is", ticker)
    API_KEY = os.getenv("SEC_API_KEY")
    query = {
        "query":  f"formType:\"10-Q\" OR formType:\"10-K\" AND ticker:{ticker}",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}],
    }
    
    print(query)
    # 2. Execute query
    query_api = QueryApi(api_key=API_KEY)
    response = query_api.get_filings(query)

    if not response["filings"]:
        return 

    # 3. Get latest filing URL
    latest_filing = response["filings"][0]
    url = latest_filing["linkToFilingDetails"]
    path = url.split("data/")[1]
    print("Extracted path:", path)  
    return path

def download_latest_filing(ticker):
    load_dotenv() 
    print("ticker is", ticker)
    base_url = " https://archive.sec-api.io/"
    # 1. Configure query for 10-K/10-Q filings
    path = find_filing(ticker)
    if not path:
        return "No filings found"
    
    API_KEY = os.getenv("SEC_API_KEY")
    download_url = base_url + path
    headers= {"Authorization": API_KEY}
    print(download_url)
    resp = requests.get(download_url, headers=headers)
    if resp.status_code == 200:
        #TODO: for some reason these are coming back as xml files sometimes - need to improve logic here.
        file_name = f"filings/{ticker}_latest.htm"
        with open(file_name, 'wb') as f:
            f.write(resp.content)
        print("File saved successfully.")
        return file_name
  
   
    return "Something Went Wrong"

import requests # Import the requests library for making HTTP requests.
import os       # Import the os module for interacting with the operating system (e.g., environment variables).
import identify_ticker # Import the 'identify_ticker' module (likely containing the ticker identification logic).
from identify_ticker import ticker_identify # Specifically import the 'ticker_identify' function from the 'identify_ticker' module.

# Retrieve the Alpha Vantage API key from the environment variable named 'ALPHA_VANTAGE_API_KEY'.
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
# Check if the API key was successfully retrieved. If not, raise a ValueError.
if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Alpha Vantage API key not found in environment variables.")

# Define the 'tickerprice' function, which takes a stock ticker symbol as input.
def tickerprice(ticker):
    # Define the base URL for the Alpha Vantage API.
    base_url = f"https://www.alphavantage.co/query"
    # Define the parameters for the API request.
    # 'apikey': Your Alpha Vantage API key for authentication.
    # 'function': Specifies the API endpoint to use, which is 'GLOBAL_QUOTE' for fetching real-time quote data.
    # 'symbol': The stock ticker symbol for which to retrieve the quote.
    params = {
        "apikey": ALPHA_VANTAGE_API_KEY,
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
    }
    # Send an HTTP GET request to the Alpha Vantage API with the specified URL and parameters.
    response = requests.get(base_url, params=params)
    # Raise an HTTPError for bad responses (4xx or 5xx status codes).
    response.raise_for_status()
    # Parse the JSON response from the API into a Python dictionary.
    data = response.json()
    # The following lines were commented out, likely used for debugging to inspect the full API response.
    # print("Full JSON Response:")
    # print(data)  # Print the entire response for inspection
    # Check if the 'Global Quote' key exists in the parsed JSON data and if its value is not empty.
    if "Global Quote" in data and data["Global Quote"]:
        # Access the 'Global Quote' dictionary.
        globalQuote = data["Global Quote"]
        # Check if the key '05. price' exists within the 'Global Quote' dictionary.
        # This key typically holds the current stock price.
        if "05. price" in globalQuote:
            # Return the value associated with the '05. price' key (the current stock price as a string).
            return globalQuote["05. price"]
        else:
            # If the '05. price' key is not found, print a warning message and return None.
            print("No '05. price' key found in Global Quote")
            return None
    else:
        # If the 'Global Quote' key is not found in the main response, print an error message and return None.
        print("No 'Global Quote' key found in the response")
        return None

# if __name__ == "__main__":
#     query=input("Enter current news:")
#     ticker = ticker_identify(query)
#     price = tickerprice(ticker)
#     if price:
#         price = float(price)
#         print(f"Current price of {ticker} is: ${price:.2f}")
#     else:
#         print("No price found")
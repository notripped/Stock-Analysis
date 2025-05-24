import requests
import os
import identify_ticker
from identify_ticker import ticker_identify

ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Alpha Vantage API key not found in environment variables.")
def ticker_price_agent(ticker):
    """
    Fetches the current price of a given stock ticker using the Alpha Vantage API.

    Args:
        ticker (str): The stock ticker symbol (e.g., "TSLA", "AAPL").

    Returns:
        float: The current stock price, or None if the price cannot be retrieved
               due to an API error, invalid ticker, or missing data.
    """
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the JSON response
        data = response.json()

        # Alpha Vantage returns an empty "Global Quote" if the symbol is invalid or no data
        if "Global Quote" in data and data["Global Quote"]:
            global_quote = data["Global Quote"]
            # The current price is typically under the key "05. price"
            if "05. price" in global_quote:
                price_str = global_quote["05. price"]
                try:
                    current_price = float(price_str)
                    return current_price
                except ValueError:
                    print(f"Error: Could not convert price '{price_str}' to float for {ticker}.")
                    return None
            else:
                print(f"Warning: '05. price' not found in Global Quote for {ticker}.")
                return None
        elif "Error Message" in data:
            print(f"Alpha Vantage API Error for {ticker}: {data['Error Message']}")
            return None
        else:
            print(f"No 'Global Quote' data found for ticker: {ticker}. Response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Network or API request error for {ticker}: {e}")
        return None
    except ValueError as e: # For JSON decoding errors
        print(f"Error decoding JSON response for {ticker}: {e}")
        return None
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred for {ticker}: {e}")
        return None

if __name__ == "__main__":
    # Test with a valid ticker
    valid_ticker = "MSFT"
    price = ticker_price_agent(valid_ticker)
    if price is not None:
        print(f"The current price of {valid_ticker} is: ${price:.2f}")
    else:
        print(f"Failed to retrieve price for {valid_ticker}.")

    print("\n" + "="*30 + "\n")

    # Test with another valid ticker
    another_ticker = "GOOGL"
    price = ticker_price_agent(another_ticker)
    if price is not None:
        print(f"The current price of {another_ticker} is: ${price:.2f}")
    else:
        print(f"Failed to retrieve price for {another_ticker}.")

    print("\n" + "="*30 + "\n")

    # Test with an invalid ticker
    invalid_ticker = "INVALIDSTOCK"
    price = ticker_price_agent(invalid_ticker)
    if price is None:
        print(f"Successfully handled invalid ticker: {invalid_ticker} (price not found).")

    print("\n" + "="*30 + "\n")

    # Test with a ticker that might hit rate limit (if you run too many times quickly)
    # Note: Alpha Vantage free tier has a limit of 5 calls per minute, 500 calls per day.
    # Be mindful when testing.
    # limited_ticker = "IBM"
    # price = ticker_price_agent(limited_ticker)
    # if price is not None:
    #     print(f"The current price of {limited_ticker} is: ${price:.2f}")
    # else:
    #     print(f"Failed to retrieve price for {limited_ticker}.")
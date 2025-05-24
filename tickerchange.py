import requests # For making HTTP requests to APIs.
import os       # For interacting with the operating system, like environment variables.
from datetime import datetime, timedelta # For handling date and time calculations.

# Retrieve the Alpha Vantage API key from the environment variable.
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
# Check if the API key is set. If not, raise an error.
if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Alpha Vantage API key not found in environment variables. "
                     "Please set ALPHA_VANTAGE_API_KEY.")

# Function to get the price change of a stock over a specified timeframe.
def tickerpricechange(ticker, timeframe="today"):
    # Base URL for the Alpha Vantage API.
    base_url = "https://www.alphavantage.co/query"
    # Convert the timeframe to lowercase for case-insensitive comparison.
    timeframe_lower = timeframe.lower()

    try:
        # Handle the case for 'today' price change.
        if timeframe_lower == "today":
            # Parameters for the GLOBAL_QUOTE endpoint.
            params = {
                "apikey": ALPHA_VANTAGE_API_KEY,
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                # 'outputsize' is not a valid parameter for GLOBAL_QUOTE.
            }
            # Make the API request.
            response = requests.get(base_url, params=params)
            # Raise an exception for HTTP errors (4xx or 5xx status codes).
            response.raise_for_status()
            # Parse the JSON response.
            data = response.json()

            # Check if 'Global Quote' data is present in the response.
            if "Global Quote" in data and data["Global Quote"]:
                # Extract the current price and previous close price as strings.
                price_str = data["Global Quote"].get("05. price")
                previous_close_str = data["Global Quote"].get("08. previous close")

                # Check if both price and previous close are available.
                if price_str and previous_close_str:
                    try:
                        # Convert the price strings to floats for calculation.
                        price = float(price_str)
                        previous_close = float(previous_close_str)
                        # Calculate the absolute change in price.
                        change = price - previous_close
                        # Calculate the percentage change, avoiding division by zero.
                        percent_change = (change / previous_close) * 100 if previous_close != 0 else 0.0
                        # Return a formatted string with the price change for today.
                        return f"${change:.2f} ({percent_change:.2f}%) for today"
                    except ValueError:
                        print(f"Error: Could not convert price or previous close to float for {ticker} today.")
                        return None
                else:
                    print(f"Could not retrieve current price or previous close for {ticker} today.")
                    return None
            # Handle API error messages.
            elif "Error Message" in data:
                print(f"Alpha Vantage API Error for {ticker} (today): {data['Error Message']}")
                return None
            # Handle cases where 'Global Quote' data is not found.
            else:
                print(f"No 'Global Quote' data found for {ticker} today. Response: {data}")
                return None

        # Handle timeframes 'last week', 'last month', 'last year'.
        elif timeframe_lower in ["last week", "last month", "last year"]:
            # Use the TIME_SERIES_DAILY endpoint for historical data.
            function = "TIME_SERIES_DAILY"
            # Parameters for the TIME_SERIES_DAILY endpoint.
            params = {
                "function": function,
                "symbol": ticker,
                "apikey": ALPHA_VANTAGE_API_KEY,
                "outputsize": "full"  # Retrieve the full historical data.
            }
            # Make the API request.
            response = requests.get(base_url, params=params)
            # Raise an exception for HTTP errors.
            response.raise_for_status()
            # Parse the JSON response.
            data = response.json()

            # Check if 'Time Series (Daily)' data is present.
            if "Time Series (Daily)" in data:
                daily_data = data["Time Series (Daily)"]
                # Sort dates from newest to oldest.
                dates = sorted(daily_data.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=True)

                # Handle cases where no daily data is available.
                if not dates:
                    print(f"No daily data available for {ticker}.")
                    return None

                # Get the most recent trading day.
                end_date_str = dates[0]
                # Get the closing price for the most recent day.
                end_price_str = daily_data[end_date_str].get("4. close")

                # Calculate the target start date based on the timeframe.
                start_date_target = None
                if timeframe_lower == "last week":
                    start_date_target = datetime.strptime(end_date_str, '%Y-%m-%d') - timedelta(days=7)
                elif timeframe_lower == "last month":
                    start_date_target = datetime.strptime(end_date_str, '%Y-%m-%d') - timedelta(days=30)
                elif timeframe_lower == "last year":
                    start_date_target = datetime.strptime(end_date_str, '%Y-%m-%d') - timedelta(days=365)

                start_price_str = None
                # Find the closing price for the closest trading day on or before the target start date.
                for date_str in dates:
                    current_date = datetime.strptime(date_str, '%Y-%m-%d')
                    if current_date <= start_date_target:
                        start_price_str = daily_data[date_str].get("4. close")
                        break

                # Check if both start and end prices were found.
                if end_price_str and start_price_str:
                    try:
                        # Convert the price strings to floats.
                        end_price = float(end_price_str)
                        start_price = float(start_price_str)

                        # Avoid division by zero for percentage change.
                        if start_price == 0:
                            print(f"Start price for {ticker} was zero for {timeframe_lower}, cannot calculate percentage change.")
                            absolute_change = end_price - start_price
                            return f"${absolute_change:.2f} (N/A%) {timeframe_lower}"
                        else:
                            # Calculate absolute and percentage change.
                            absolute_change = end_price - start_price
                            percentage_change = (absolute_change / start_price) * 100
                            # Return a formatted string with the price change over the specified timeframe.
                            return f"${absolute_change:.2f} ({percentage_change:.2f}%) {timeframe_lower}"
                    except ValueError:
                        print(f"Error converting historical price strings to float for {ticker} {timeframe_lower}.")
                        return None
                else:
                    print(f"Could not retrieve valid start or end price for {ticker} {timeframe_lower}.")
                    return None
            # Handle API error messages for historical data.
            elif "Error Message" in data:
                print(f"Alpha Vantage API Error for {ticker} ({timeframe_lower}): {data['Error Message']}")
                return None
            # Handle cases where historical data is not found.
            else:
                print(f"No 'Time Series (Daily)' data found for {ticker} {timeframe_lower}. Response: {data}")
                return None

        # Handle invalid timeframe inputs.
        else:
            print(f"Invalid timeframe: '{timeframe}'. Supported values are 'today', 'last week', 'last month', 'last year'.")
            return None

    # Catch various exceptions that might occur during the API request or data processing.
    except requests.exceptions.RequestException as e:
        print(f"Network or API request error for {ticker} ({timeframe}): {e}")
        return None
    except ValueError as e: # For JSON decoding errors or other conversion issues
        print(f"Error processing data for {ticker} ({timeframe}): {e}")
        return None
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred for {ticker} ({timeframe}): {e}")
        return None
# if __name__ == "__main__":
#     ticker=input("Enter the ticker symbol you wish to analyze: ")
#     timeframe=input("Enter the timeframe you wish to analyze out of today,last week,last month,last year: ")
#     print(f"The change for {ticker} in {timeframe} is:",tickerpricechange(ticker,timeframe=timeframe))

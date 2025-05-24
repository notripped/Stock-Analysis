import requests  # Import the requests library for making HTTP requests to web APIs.
import os  # Import the os module to interact with the operating system, specifically for environment variables.

# Import the 'identify_ticker' module and the 'ticker_identify' function from it.
# This import is present in your provided code, but for the 'ticker_news_agent'
# itself, these specific imports are not directly used. They would be used by
# an orchestrator agent that calls 'ticker_news_agent'.
import identify_ticker
from identify_ticker import ticker_identify

# Retrieve the Alpha Vantage API key from environment variables.
# It's crucial for authenticating requests to the Alpha Vantage API.
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
# If the API key is not found, raise a ValueError to stop execution and inform the user.
if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Alpha Vantage API key not found in environment variables.")


# Define the ticker_news_agent function.
# Objective: Retrieves recent news articles related to a given stock ticker.
# Args:
#   ticker (str): The stock ticker symbol (e.g., "AAPL", "MSFT").
#   max_articles (int, optional): The maximum number of news articles to retrieve. Defaults to 5.
# Returns:
#   list of dict: A list of dictionaries, each representing a news article with details like title, URL, source, summary, and sentiment.
#   None: If an error occurs during the API call, no news is found, or the response is invalid.
def ticker_news_agent(ticker, max_articles=5):
    # Define the base URL for the Alpha Vantage API.
    base_url = "https://www.alphavantage.co/query"

    # Define the parameters for the API request.
    # "function": "NEWS_SENTIMENT" specifies the desired API endpoint for news and sentiment data.
    # "tickers": ticker passes the stock symbol for which news is requested.
    # "apikey": ALPHA_VANTAGE_API_KEY includes the authentication key.
    # "limit": max_articles controls the number of news items returned.
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "limit": max_articles  # Limit the number of results to keep output concise.
    }

    try:
        # Send an HTTP GET request to the Alpha Vantage API with the defined parameters.
        response = requests.get(base_url, params=params)

        # Raise an HTTPError for bad responses (4xx or 5xx status codes).
        # This helps in immediately identifying issues like rate limits, invalid keys, etc.
        response.raise_for_status()

        # Parse the JSON response from the API into a Python dictionary.
        data = response.json()

        # Check if the "feed" key exists in the response.
        # The "feed" key contains the list of news articles.
        if "feed" in data:
            news_articles = []  # Initialize an empty list to store processed news articles.
            # Iterate through each news item in the "feed".
            for item in data["feed"]:
                # Append a dictionary for each article, extracting relevant fields.
                # .get() is used for safe access, returning None if a key doesn't exist,
                # preventing KeyError. For sentiment, it handles nested dictionaries.
                news_articles.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "source": item.get("source"),
                    "summary": item.get("summary"),
                    "sentiment_label": item.get("sentiment", {}).get("label"),  # Access nested sentiment label
                    "sentiment_score": item.get("sentiment", {}).get("score")  # Access nested sentiment score
                })
            return news_articles  # Return the list of extracted news articles.
        else:
            # If "feed" key is not found, it means no news was returned for the ticker.
            print(f"No news found for ticker: {ticker}")
            return None  # Return None to indicate no news was found.

    except requests.exceptions.RequestException as e:
        # Catch any request-related errors (e.g., network issues, invalid URL, HTTP errors).
        print(f"Error fetching news for {ticker}: {e}")
        return None  # Return None on request failure.
    except ValueError as e:
        # Catch errors that occur if the API response is not valid JSON.
        print(f"Error decoding JSON response for {ticker}: {e}")
        return None  # Return None on JSON decoding failure.

# if __name__ == "__main__":
#     # stock_ticker = "AAPL"
#     # news = ticker_news_agent(stock_ticker)
#     query=input("Enter a query related to a company")
#     stock_ticker=ticker_identify(query)
#     news = ticker_news_agent(stock_ticker)
#     if news:
#         print(f"Recent news for {stock_ticker}:")
#         for article in news:
#             print("-" * 40)
#             print(f"Title: {article['title']}")
#             print(f"Source: {article['source']}")
#             print(f"URL: {article['url']}")
#             if article.get('summary'):
#                 print(f"Summary: {article['summary']}")
#             if article.get('sentiment_label'):
#                 print(f"Sentiment: {article['sentiment_label']} ({article['sentiment_score']})")
#         print("-" * 40)
#     else:
#         print(f"Could not retrieve news for {stock_ticker}.")

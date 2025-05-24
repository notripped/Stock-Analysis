import google.generativeai as genai # Import the Google Generative AI library.
import os # Import the os module for environment variables.
from identify_ticker import ticker_identify # Import the function to identify stock tickers from text.
from ticker_news import ticker_news_agent # Import the function to fetch news about a stock.
from tickeranalysis import tickeranalysis # Import the function to analyze stock price movements based on news.
from tickerprice import tickerprice # Import the function to get the current price of a stock.
from tickerchange import tickerpricechange # Import the function to get the price change of a stock over a period.

# Configure the Generative AI library with the API key from the environment variable 'GOOGLE_API_KEY'.
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Initialize the Gemini Flash model for orchestrating the agents.
orchestrator_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Define the StockAnalysisOrchestrator class to manage and route user queries to the appropriate sub-agents.
class StockAnalysisOrchestrator:
    def __init__(self):
        pass # Currently no initialization logic needed for the orchestrator.

    # Method to process a user's natural language query and coordinate with sub-agents.
    def process_query(self, user_query):
        # Define a prompt for the language model to understand the user's intent and extract entities.
        intent_prompt = f"""You are an expert at understanding user queries related to stock analysis.
        Identify the main intent of the query and any relevant entities like stock tickers and timeframes.

        Examples:
        User: Why did Tesla stock drop today?
        Intent: Investigate price drop reason
        Ticker: TSLA
        Timeframe: today

        User: What's happening with Palantir stock recently?
        Intent: Get recent news
        Ticker: PLTR
        Timeframe: recently

        User: How has Nvidia stock changed in the last 7 days?
        Intent: Get price change
        Ticker: NVDA
        Timeframe: last week

        User: What is the current price of Apple?
        Intent: Get current price
        Ticker: AAPL

        User: Tell me something about Google's stock.
        Intent: Get general information
        Ticker: GOOGL

        User: Did Amazon's price go up last month?
        Intent: Analyze price change direction
        Ticker: AMZN
        Timeframe: last month

        User Query: {user_query}
        Intent:
        Ticker:
        Timeframe:"""

        try:
            # Send the intent recognition prompt to the language model.
            intent_response = orchestrator_model.generate_content(intent_prompt)
            # Extract the text response and remove leading/trailing whitespace.
            intent_text = intent_response.text.strip()
            # Initialize a dictionary to store the extracted intent parts.
            intent_parts = {}
            # Parse the response text, splitting it into lines and then key-value pairs.
            for line in intent_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    intent_parts[key.strip()] = value.strip()

            # Extract the identified intent, ticker text, and raw timeframe from the parsed parts.
            intent = intent_parts.get("Intent")
            ticker_text = intent_parts.get("Ticker")
            timeframe_raw = intent_parts.get("Timeframe", "today").lower()
            # Normalize the timeframe by removing "last " prefix for easier processing.
            timeframe_normalized = timeframe_raw.replace("last ", "") if "last" in timeframe_raw else timeframe_raw

            # If no ticker is identified, return an error message.
            if not ticker_text:
                return "Could not identify the stock ticker in your query."

            # Use the ticker_identify sub-agent to resolve the ticker text to a standard symbol.
            ticker = ticker_identify(ticker_text)
            # If the ticker cannot be resolved, return an error message.
            if not ticker:
                return f"Could not resolve the ticker for '{ticker_text}'."

            # Subagent Selection and Invocation based on the identified intent.
            if intent and "price drop reason" in intent.lower():
                # If the intent is to investigate a price drop, call the tickerpricechange and ticker_news agents.
                price_change_result = tickerpricechange(ticker, "today")
                news_result = ticker_news_agent(ticker)
                # If both price change and news are available, call the tickeranalysis agent.
                if price_change_result and news_result:
                    return tickeranalysis(ticker, "today")
                else:
                    return "Could not retrieve enough information for analysis."
            elif intent and "get recent news" in intent.lower():
                # If the intent is to get recent news, call the ticker_news_agent.
                news_result = ticker_news_agent(ticker)
                if news_result:
                    # Format and return the recent news headlines.
                    return f"Recent news for {ticker}:\n" + "\n".join([f"- {item['title']}" for item in news_result])
                else:
                    return f"No recent news found for {ticker}."
            elif intent and "get price change" in intent.lower():
                # If the intent is to get the price change over a specific period.
                if timeframe_normalized in ["week", "month", "year"]:
                    full_timeframe = f"last {timeframe_normalized}"
                    price_change_result = tickerpricechange(ticker, full_timeframe)
                    if price_change_result:
                        return f"Price change for {ticker} over the {full_timeframe}: {price_change_result}"
                    else:
                        return f"Could not retrieve price change information for {ticker} for the {full_timeframe}."
                elif timeframe_normalized == "today":
                    price_change_result = tickerpricechange(ticker, timeframe_normalized)
                    if price_change_result:
                        return f"Price change for {ticker} for today: {price_change_result}"
                    else:
                        return f"Could not retrieve price change information for {ticker} for today."
                else:
                    return "Sorry, I cannot handle that specific timeframe for price change."
            elif intent and "get current price" in intent.lower():
                # If the intent is to get the current price, call the tickerprice agent.
                price_result = tickerprice(ticker)
                if isinstance(price_result, float):  # Ensure the result is a float before formatting.
                    return f"The current price of {ticker} is: ${price_result:.2f}"
                elif isinstance(price_result, str):
                    return f"Error retrieving current price: {price_result}" # Handle potential string errors.
                else:
                    return f"Could not retrieve the current price for {ticker}."
            elif intent and "get general information" in intent.lower():
                # If the intent is to get general information, call the ticker_news agent to get recent news.
                news_result = ticker_news_agent(ticker)
                if news_result:
                    # Format and return recent news titles and summaries.
                    return f"Here's some recent information about {ticker}:\n" + "\n".join([f"- {item['title']}: {item.get('summary', 'No summary available.')}" for item in news_result])
                else:
                    return f"No recent information found for {ticker}."
            elif intent and "analyze price change direction" in intent.lower():
                # If the intent is to analyze the direction of price change over a period.
                if timeframe_normalized in ["week", "month", "year"]:
                    full_timeframe = f"last {timeframe_normalized}"
                    price_change_result = tickerpricechange(ticker, full_timeframe)
                    if price_change_result:
                        # Basic analysis of the direction based on the presence of '+' or '-' in the result string.
                        if "+" in price_change_result:
                            return f"Amazon's price went up last {timeframe_normalized}."
                        elif "-" in price_change_result:
                            return f"Amazon's price went down last {timeframe_normalized}."
                        elif "(0.00%)" in price_change_result:
                            return f"Amazon's price remained relatively unchanged last {timeframe_normalized}."
                        else:
                            return f"Could determine the price direction for Amazon last {timeframe_normalized}."
                    else:
                        return f"Could not retrieve price change information for Amazon for last {timeframe_normalized}."
                else:
                    return "Sorry, I can only analyze price change direction for 'last week', 'last month', or 'last year'."
            else:
                return "Sorry, I'm not sure how to handle that query."

        except Exception as e:
            return f"An error occurred: {e}"

# Example Usage when the script is run directly.
if __name__ == "__main__":
    orchestrator = StockAnalysisOrchestrator()

    queries = [
        "How has Nvidia stock changed in the last week?",
        "What is the current price of Apple?",
        "Tell me something about Google's stock.",
        "Did Amazon's price go up last month?",
        "How has Tesla stock changed in the last year?"
    ]

    for query in queries:
        response = orchestrator.process_query(query)
        print(f"\nQuery: {query}")
        print(f"Response: {response}")
import google.generativeai as genai
import os

# Configure the Generative AI model with the API key stored in the environment variables.
# It assumes you have set an environment variable named 'GEMINI_API_KEY' with your API key.
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Specify the name of the Gemini model to use.
model_name = "models/gemini-1.5-flash-latest"
# Initialize the GenerativeModel with the specified model name.
model = genai.GenerativeModel(model_name)

# Define a function called 'ticker_identify' that takes a user query as input.
def ticker_identify(user_query):
    # Define a prompt to instruct the language model to identify the stock ticker
    # symbol from the user's query.
    prompt = f"""You are a helpful agent designed to identify the stock ticker symbol
       from the user's query. If the query clearly mentions a stock, extract its
       ticker symbol. If the query mentions a company name, try to identify its
       most common ticker symbol.

       Examples:
       User: What's the latest on Apple stock?
       Ticker: AAPL

       User: Tell me about Google.
       Ticker: GOOGL

       User: Price of Microsoft today?
       Ticker: MSFT

       User: How is Amazon doing?
       Ticker: AMZN

       User: Any news about Berkshire Hathaway?
       Ticker: BRK.A

       User Query: {user_query}
       Ticker: """

    try:
        # Send the prompt to the language model to generate a response.
        response = model.generate_content(prompt)
        # Extract the generated text (which should be the ticker symbol) and remove any leading/trailing whitespace.
        ticker = response.text.strip()
        # Basic validation to check if the identified ticker looks like a valid stock ticker.
        # It checks if the length is between 1 and 10 characters, and if it's fully uppercase
        # or contains a period (which is common for some tickers like BRK.A).
        if 1 <= len(ticker) <= 10 and (ticker.isupper() or "." in ticker):
            return ticker  # Return the identified ticker symbol.
        else:
            return None  # Return None if the identified text doesn't look like a valid ticker.
                         # This indicates that the ticker could not be reliably identified.
    except Exception as e:
        # If any error occurs during the communication with the language model,
        # print the error message for debugging purposes and return None.
        print(f"Error in identify_ticker_agent: {e}")
        return None

# queries = [
#     "What's the latest on Microsoft?",
#     "Tell me about Tesla stock.",
#     "What about Google?",
#     "How has Apple performed this week?",
#     "Something about General Electric.",
#     "The weather in New York.",
#     "Talk about Berkshire Hathaway class B shares." # Might need more sophisticated handling for class B
# ]
#
# for query in queries:
#     ticker = ticker_identify(query)
#     if ticker:
#         print(f"User Query: '{query}' -> Identified Ticker: '{ticker}'")
#     else:
#         print(f"User Query: '{query}' -> Ticker not found.")
# query=input("Enter a query:")
# ticker=ticker_identify(query)
# if ticker:
#     print(query,":",ticker)
# else:
#     print(query,":ticker not found")
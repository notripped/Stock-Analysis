import google.generativeai as genai # Import the Google Generative AI library for interacting with language models.
import os # Import the os module for accessing environment variables (like API keys).
from datetime import datetime # Import the datetime class for working with dates and times (though not directly used in this function).
from ticker_news import ticker_news_agent # Import the function to fetch news articles for a given ticker.
from tickerchange import tickerpricechange # Import the function to fetch the price change for a given ticker over a timeframe.

# Configure the Generative AI library with the API key stored in the 'GEMINI_API_KEY' environment variable.
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Specify the name of the Gemini model to be used for analysis.
model_name = "models/gemini-1.5-flash-latest"
# Initialize the GenerativeModel with the specified model name.
model = genai.GenerativeModel(model_name)

# Define the 'tickeranalysis' function, which takes a stock ticker and an optional timeframe as input.
# It aims to analyze the reasons behind recent stock price movements.
def tickeranalysis(ticker, timeframe="today"):
    # Fetch recent news articles for the given ticker, limiting the number of articles to 5.
    news = ticker_news_agent(ticker, max_articles=5)
    # Fetch the price change for the given ticker over the specified timeframe.
    price_change = tickerpricechange(ticker, timeframe=timeframe)

    # Check if either news data or price change data could not be retrieved.
    if news is None or price_change is None:
        print(f"Insufficient data to analyze {ticker} for {timeframe}.")
        return None # Return None if there's not enough data for analysis.

    # Extract the titles of the news articles into a list.
    newshead = [article.get("title") for article in news if article.get("title")]
    # Create a list of strings containing the news title along with its sentiment label and score (if available).
    news_sentiment = [
        f"{article.get('title')} (Sentiment: {article.get('sentiment_label')}, Score: {article.get('sentiment_score')})"
        for article in news if article.get('title')]

    # Define a detailed prompt for the language model to perform the stock analysis.
    prompt = f"""You are a senior financial analyst tasked with providing a detailed explanation of the recent price movements
  of the stock with ticker '{ticker}' over the last {timeframe}. Your analysis should integrate recent news,
  price changes, and potential market factors.

  **1. Price and Volume Context:**
  Briefly state the observed price change: '{price_change}'. If available in the `ticker_price_change_agent` output (consider adding volume data if the API provides it), also mention any significant changes in trading volume during this period.

  **2. Recent News Analysis:**
  Review the following recent news items related to '{ticker}':
  News:
  {chr(10).join(news_sentiment) if news_sentiment else 'No significant news found.'}

  For each significant news item, consider its potential impact on the stock price. Note the sentiment (positive, negative, neutral) and the source's credibility if possible.

  **3. Correlation and Causation:**
  Analyze the relationship between the observed price change and the recent news. Are there any apparent correlations? Discuss potential causal links, being careful not to assume direct causation without strong evidence. Consider:
  - Did positive news coincide with price increases?
  - Did negative news coincide with price decreases?
  - Were there any major news events without a corresponding price reaction, and why might that be?

  **4. Broader Market Context (If Applicable):**
  If you have access to information about broader market trends or sector-specific news during this period (you might need to fetch this with another agent in a more advanced system), briefly consider if these factors might have influenced the stock's movement independently of company-specific news.

  **5. Summary of Key Drivers:**
  Based on your analysis, provide a detailed summary of the most likely reasons behind the observed price movement. Prioritize the most significant factors and explain your reasoning. If the price movement seems uncorrelated with the available news, state this and suggest potential reasons (e.g., broader market forces, technical trading, information not yet publicly available).

  **Example of a more detailed analysis point:**
  "The stock experienced a significant increase of X% over the last {timeframe}. This coincided with the release of a highly positive earnings report on [Date], which highlighted strong revenue growth and increased profitability. Analyst upgrades following this report further fueled positive sentiment. However, a negative article from [Source] regarding potential regulatory challenges emerged mid-week, which may have tempered some of the gains."

  Your detailed analysis summary:"""

    try:
        # Send the detailed prompt to the language model to generate the analysis.
        response = model.generate_content(prompt)
        # Return the generated text analysis, removing any leading or trailing whitespace.
        return response.text.strip()
    except Exception as e:
        # If any error occurs during the analysis process with the language model,
        # print the error message for debugging and return None.
        print(f"Error during analysis for {ticker} ({timeframe}): {e}")
        return None

# if __name__ == "__main__":
#     ticker = "TSLA"
#     timeframe_today = "today"
#     timeframe_week = "last week"
#
#     print(f"--- Analyzing {ticker} for {timeframe_today} ---")
#     analysis_today = tickeranalysis(ticker, timeframe_today)
#     if analysis_today:
#         print(analysis_today)
#     else:
#         print(f"Could not analyze {ticker} for {timeframe_today}.")
#
#     print(f"\n--- Analyzing {ticker} for {timeframe_week} ---")
#     analysis_week = tickeranalysis(ticker, timeframe_week)
#     if analysis_week:
#         print(analysis_week)
#     else:
#         print(f"Could not analyze {ticker} for {timeframe_week}.")
# Stock Analysis Agent with Google Gemini and Alpha Vantage

This repository contains a set of Python agents designed to analyze stock market information using the Google Gemini language model and the Alpha Vantage API for financial data.

## Overview

This project implements a multi-agent system where different agents collaborate to answer user queries related to stock analysis. The system includes agents for:

-   **Identifying Stock Tickers:** Extracts stock ticker symbols from natural language queries using Google Gemini.
-   **Fetching News Sentiment:** Retrieves recent news articles and their sentiment analysis for a given ticker from Alpha Vantage.
-   **Getting Current Stock Price:** Fetches the real-time price of a stock from Alpha Vantage.
-   **Getting Stock Price Change:** Calculates the price change of a stock over different timeframes (today, last week, last month, last year) using Alpha Vantage data.
-   **Analyzing Stock Price Movements:** Correlates recent news sentiment with stock price changes using Google Gemini to provide insights into the likely reasons for price movements.
-   **Orchestrating the Agents:** A central orchestrator agent uses Google Gemini to understand user intent and routes queries to the appropriate sub-agents, managing the flow of information.

## Files in the Repository

-   `identify_ticker.py`: Contains the `ticker_identify` agent, which uses Google Gemini to extract stock tickers from user queries.
-   `ticker_news.py`: Contains the `ticker_news_agent`, which fetches recent news and sentiment data from Alpha Vantage.
-   `tickerprice.py`: Contains the `tickerprice` agent, which retrieves the current stock price from Alpha Vantage.
-   `tickerchange.py`: Contains the `tickerpricechange` agent, which calculates the price change over different timeframes using Alpha Vantage historical data.
-   `tickeranalysis.py`: Contains the `tickeranalysis` agent, which uses Google Gemini to analyze the relationship between news and price movements.
-   `orchestrator.py`: Contains the `StockAnalysisOrchestrator` agent, which handles user queries and orchestrates the calls to other sub-agents.
-   `README.md`: This file, providing an overview of the project.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```
    (Replace `YOUR_USERNAME/YOUR_REPOSITORY_NAME` with the actual repository URL)

2.  **Install Dependencies:**
    ```bash
    pip install google-generativeai requests python-dotenv
    ```

3.  **Set up Environment Variables:**
    -   Create a `.env` file in the root of the repository.
    -   Add your Google Gemini API key and Alpha Vantage API key to the `.env` file:
        ```dotenv
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY
        ```
        (Replace `YOUR_GEMINI_API_KEY` and `YOUR_ALPHA_VANTAGE_API_KEY` with your actual API keys.)

4.  **Run the Orchestrator (Example):**
    ```bash
    python orchestrator.py
    ```
    The `orchestrator.py` script includes example usage in its `if __name__ == "__main__":` block. You can modify the `queries` list to test different scenarios.

## API Keys

-   **Google Gemini API Key:** You will need a Google Cloud project with access to the Generative AI models and an API key. Follow the Google Cloud documentation to set this up.
-   **Alpha Vantage API Key:** You will need to sign up for a free API key from Alpha Vantage at [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key).

**Important:** Keep your API keys secure and do not commit them directly to your repository. Using a `.env` file and ensuring it's in your `.gitignore` is recommended.

## Usage

The `orchestrator.py` script demonstrates how to use the `StockAnalysisOrchestrator` to process different types of user queries. You can interact with the orchestrator by providing natural language questions about stock information.

**Example Queries:**

-   "Why did Tesla stock drop today?"
-   "What's happening with Palantir stock recently?"
-   "How has Nvidia stock changed in the last week?"
-   "What is the current price of Apple?"
-   "Tell me something about Google's stock."
-   "Did Amazon's price go up last month?"

The orchestrator will route these queries to the appropriate sub-agents and return a response based on the available data and the analysis performed by Google Gemini.

## Limitations and Future Work

-   **API Rate Limits:** The Alpha Vantage API has rate limits, especially on the free tier. The application might encounter issues if too many requests are made in a short period. Consider implementing caching or upgrading to a premium plan for production use.
-   **News Sentiment Accuracy:** The sentiment analysis provided by Alpha Vantage might not always be perfectly accurate, which could affect the analysis performed by the `tickeranalysis` agent.
-   **Broader Market Context:** The current `tickeranalysis` agent has a placeholder for considering broader market context but does not actively fetch this data. Future work could involve integrating with other APIs to get market indices or sector-specific news.
-   **Volume Data:** The `tickeranalysis` agent's prompt mentions volume data, but the current `tickerchange` agent does not retrieve this information. This could be added in the future for more comprehensive analysis.
-   **Error Handling:** While basic error handling is implemented, more robust error management and logging could be added.
-   **User Interface:** Currently, the interaction is through the command line. A web interface or other user-friendly front-end could be developed.

## Contributing

Contributions to this project are welcome. Feel free to submit pull requests with bug fixes, new features, or improvements. Please follow standard Git contribution workflows.

## License

[Specify your license here, e.g., MIT License]

## Author

[Your Name/GitHub Username]

# Ensure when adding new functions, they are added to tools.json so the model knows it can use them. Also must add them to the available_functions list for execution
# Functions must take an argument, in json form from the models function call, and output must be a single string or key:value pair {}
# Add any new functions above the available_functions list
#
# functions can be defined async if necessary but for time being have kept sync/standard
#
# All function results must be passed through create_json_response before returning to the model
from typing import Any
import backend_app.services.document_retrieval.vectorstore as vectorstore
from backend_app.services.news.news_service import news_service
import asyncio
import yfinance as yf
import json
from backend_app.services.chatbot.chatbot_agents.agent_orchestrator import AgentOrchestrator
from datetime import datetime, timedelta

def create_json_response(ui_type: str = "text",
                        ui_title: str = "",
                        ui_content: Any = None,
                        response_model_content: str = "",
                        target: str = None):  # Add target parameter
    """ Generates a standardised json object for passing tool responses back to the model. 

    Any of the fields (except for ui_type) can be passed back blank. 
    
    Parameters:
    - ui_type (str): Indicates the UI object that the function will generate. Defaults to text. Must be a string. 
    - ui_title (str): The title to be displayed in the UI object. Defaults to blank. Must be a string.
    - ui_content (Any): The content to be displayed in the UI object, returned by the function call. Defaults to blank. Can take any data type (I think)
    - response_model_content (str): The response to be passed back to the model for further generation (if applicable). Defaults to blank. Must always be passed as a string.

    Returns: 
    - json_object_response (dict): a dictionary representing the JSON structure."""

    json_object_response = {
        "ui_type": ui_type,
        "ui_title": ui_title,
        "ui_content": ui_content,
        "response_content": response_model_content
    }
    
    if target:
        json_object_response["target"] = target
        
    return json_object_response

def get_stock_price(arguments):
    """
    Retrieves stock price data for a given ticker symbol on either a specified or inferred date.
    
    Parameters:
    - arguments (dict): A JSON object containing 'ticker', 'date' which is optional.
    
    Returns:
    - JSON response containing the stock price for the requested date.
    """
    try:
        arguments = json.loads(arguments)
        # Get the ticker from arguments (it's now expected to be a single string)
        ticker = arguments.get("ticker")
        date = arguments.get("date")
        
        # Set the stock ticker
        stock = yf.Ticker(ticker)

        if date:
            # If a date is provided, attempt to retrieve historical data for that specific date
            try:
                date_parsed = datetime.strptime(date, "%Y-%m-%d").date()
                next_day = date_parsed + timedelta(days=1)  # Ensure we get at least one trading day

                # Retrieve historical data for the date
                historical_data = stock.history(start=date_parsed, end=next_day)

                # Check if data exists for the exact date
                if date_parsed.strftime("%Y-%m-%d") in historical_data.index:
                    historical_price = historical_data.loc[date_parsed.strftime("%Y-%m-%d"), 'Close']
                    return create_json_response(
                        "ticker", 
                        f"Ticker: {ticker} on {date}", 
                        f"{historical_price:.2f}", 
                        response_model_content=f"The closing price of {ticker} on {date} was: ${historical_price:.2f}"
                    )
                else:
                    return create_json_response(
                        response_model_content=f"No trading data available for {ticker} on {date}. It might have been a non-trading day."
                    )
            except ValueError:
                return create_json_response(
                    response_model_content="Invalid date format. Please use YYYY-MM-DD."
                )

        current_price = stock.info.get('regularMarketPrice')
        
        # If live price is not available, fall back to the previous close price
        if current_price is None:
            current_price = stock.info.get('regularMarketPreviousClose')
            if current_price is not None:
                return create_json_response("ticker", f"Ticker: {ticker}", f"{current_price:.2f}", response_model_content=f"The market is currently closed. The last closing price of {ticker} was: ${current_price:.2f}")
            else:
                return create_json_response(response_model_content=f"Could not retrieve the current or previous close price for {ticker}.")
        else:
            result = create_json_response("ticker", f"Ticker: {ticker}", f"{current_price:.2f}")
            return result
    
    except json.JSONDecodeError as e:
        print(f"Failed to parse arguments: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return create_json_response(response_model_content="Unable to retrieve stock price.")

def get_historical_stock_data(arguments):
    """
    Retrieves historical stock price data for a given ticker symbol over a specified date range.
    
    Parameters:
    - arguments (dict): A JSON object containing 'ticker', 'start_date', and 'end_date'.
    
    Returns:
    - JSON response containing the date and closing price for each day in the specified range.
    """
    try:
        # Parse arguments
        arguments = json.loads(arguments)
        ticker = arguments.get("ticker")
        start_date = arguments.get("start_date")
        end_date = arguments.get("end_date")

        if not ticker or not start_date or not end_date:
            return create_json_response(response_model_content="Please provide a valid ticker, start date, and end date.")

        # Retrieve historical stock data from Yahoo Finance - we may need a better api but will do for now
        stock = yf.Ticker(ticker)
        historical_data = stock.history(start=start_date, end=end_date)

        # If no data is returned
        if historical_data.empty:
            return create_json_response(response_model_content=f"No historical data found for {ticker} in the specified date range.")
        
        # Extract dates and closing prices for plotting
        data_points = [
            {"date": date.strftime("%Y-%m-%d"), "close": close}
            for date, close in zip(historical_data.index, historical_data["Close"])
        ]
        
        # Return data in JSON format
        return create_json_response(
            ui_type="line_chart",
            ui_title=f"Historical data for {ticker.upper()}",
            ui_content=data_points,  # List of {date, close} dictionaries
            response_model_content=f"Successfully retrieved historical data for {ticker} from {start_date} to {end_date}."
        )
    
    except json.JSONDecodeError as e:
        print(f"Failed to parse arguments: {e}")
        return create_json_response(response_model_content="Invalid arguments. Please provide a JSON object.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return create_json_response(response_model_content="Unable to retrieve historical stock data.")

def retrieve_portfolio(user_id): 
    """Retrieves the user's portfolio given the user id.
    
    Parameters: 
    - user_id theoretically, but we don't need this yet as it will always retrieve the same portfolio.
    
    Returns:
    - a JSON string taken from ./portfolios/portfolio1.json """

    with open("./portfolios/portfolio1.json", "r") as file:
        portfolio_data = json.load(file)
    
    portfolio = json.dumps(portfolio_data) # Converts the json object in to a string to be interpreted by the model. 
    
    return create_json_response(response_model_content=portfolio)

async def get_news(arguments):
    try:
        args = json.loads(arguments)
        chat_context = {
            'message': args.get('query', ''),
            'extracted_tickers': args.get('tickers', []),
            'topics': args.get('topics', [])
        }
        
        news_summaries = await news_service.get_news_summaries(chat_context)
        
        if not news_summaries:
            return create_json_response(
                response_model_content="No relevant news found for the specified tickers."
            )

        # Create a brief summary for the chat
        tickers_str = ", ".join(args.get('tickers', []))
        
        # Send both the news data and chat message in a single response
        return create_json_response(
            ui_type="news_feed",
            ui_title="Latest News",
            ui_content=news_summaries,
            response_model_content=f"I've found {len(news_summaries)} relevant news articles about {tickers_str}. You can view them in the News panel on the right side of your screen.",
            target="news_space"
        )
    
    except Exception as e:
        print(f"Error in get_news: {e}")
        return create_json_response(response_model_content="Unable to retrieve news at this time.")
    
async def agent_orchestrator(arguments): 
    args = json.loads(arguments)
    instructions = args.get("instructions")

    agent_orchestrator = AgentOrchestrator()
    results = await agent_orchestrator.orchestrate_agents(instructions)

    # Results is returned as a list of responses (one response from each participating agent) so we need to flatten it to pass it back to the chatbot. 
    if isinstance(results, list): 
        flattened_results = ' '.join(str(result) for result in results) 

    return create_json_response(response_model_content=flattened_results)

# Map function names to actual functions, to call with execute_function_call below
available_functions = {
    "retrieve_filing": vectorstore.retrieve_filings,
    "get_stock_price": get_stock_price,
    "retrieve_portfolio" : retrieve_portfolio,
    "get_historical_stock_data" : get_historical_stock_data,
    "get_news": get_news,
    "agent_orchestrator": agent_orchestrator,
}

async def execute_function_call(function_name, arguments):
    function = available_functions.get(function_name, None)
    if function:
        if asyncio.iscoroutinefunction(function):
            results = await function(arguments)
            # Handle case where function returns multiple responses
            if isinstance(results, list):
                return results
            return results
        else:
            results = function(arguments)
    else:
        results = create_json_response(response_model_content=f"Error: function {function_name} does not exist")
    return results


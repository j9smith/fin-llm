from openai import AsyncOpenAI #import the async supported open ai client
from dotenv import load_dotenv 
import json
import datetime
from backend_app.services.chatbot import functions
import re
import os

load_dotenv()
aclient = AsyncOpenAI()

system_prompt = f"Today's date is {datetime.date.today()}. The You are a friendly CFA level financial advisor and analyst first and foremost. Respond in a technical, information-dense format, using specific data points, facts, and figures where applicable. Use available context to answer comprehensively, avoiding the need for follow-up questions. For specific questions, provide detailed techincal analyses where you can. For broader queries, provide a short but comprehensive overview that offers the user the opportunity to delve deeper. Sound like a professional analyst - assume the user is knowledgeable about finance (including investing). Avoid being overly polite. Be concise. You have tools at your disposal, use them liberally - they will give you access to regulatory filings and up-to-date stock prices. Every public company should be formatted as [CompanyName (TICKER)](/company/TICKER) in every instance, including lists and sentences. Example: [Apple (AAPL)](/company/AAPL), [Tesla (TSLA)](/company/TSLA), etc. If the company is not publicly traded, use the format [CompanyName (Private)](/company/CompanyName) instead, like so: [Holtec (Private)](/company/Holtec)"
model_choice = "gpt-4o-mini"
messages = [{"role": "system", "content": system_prompt}]

file_path = os.path.join(os.path.dirname(__file__), "tools.json")
with open(file_path, "r") as tools_file:
    tools = json.load(tools_file)

async def get_chatgpt_stream(chat_history):
    # Parsing chat history and adding to messages list for correct formatting
    parse_and_add_messages(chat_history)

    try:
        # Creating completions chat
        response = create_completions_chat(model_choice, messages, "auto")

        # Compile function calls list with function id's, names, and arguments
        function_calls = []
        async for chunk in response:
            # Grabbing token usage
            if not chunk.choices:
                print(f"Total token usage: {chunk.usage.total_tokens}") # Can also add prompt tokens and completion tokens
                continue

            chunk = chunk.choices[0].delta
            # Returning regular responses
            if chunk.content:
                yield chunk.content
            # Grabbing function id and name
            elif chunk.tool_calls and chunk.tool_calls[0].function.name:
                function_id = chunk.tool_calls[0].id
                function_name = chunk.tool_calls[0].function.name
                function_arguments = "" # Clearing argument from previous call, if there was one
                function_list = [function_id, function_name, function_arguments]
                function_calls.append(function_list)
            # Grabbing function arguments
            elif chunk.tool_calls:
                function_index = chunk.tool_calls[0].index
                function_arguments += chunk.tool_calls[0].function.arguments # Creating arguments string with each chunk
                function_calls[function_index][2] = function_arguments # Replacing argument value in list, until its complete

        # Check if function_calls exists, and if its a single list then wrap it for the loop below
        if function_calls and not isinstance(function_calls[0], list):
            function_calls = [function_calls]

        tools_output = 0

        # Process each function call in function calls
        for function_call in function_calls:
            print(f"Calling function: {function_call[1]}, args: {function_call[2]}")
            tool_output = await functions.execute_function_call(function_call[1], function_call[2]) # Tool output is returned as a dict, await as the ex_fn_call is async
            if(tool_output["ui_type"] != "text"): # ui_type 'text' are treated as normal - this indicates no special UI is required 
                yield tool_output
            tool_output_content = tool_output["response_content"] # The content relevant for the model is extracted and passed back into the model
            tools_output += 1
            messages.append({
                "role": "function",
                "tool_call_id": function_call[0],
                "name": function_call[1],
                "content": tool_output_content
            })

        # Check if tools_output list contains as values, if it does pass it back to the model to stream its response
        if tools_output > 0:
            response = create_completions_chat(model_choice, messages, "none")
            async for chunk in response:
                # Grabbing token usage
                if not chunk.choices:
                    print(f"Total token usage: {chunk.usage.total_tokens}") # Can also add prompt tokens and completion tokens
                # Returning response
                elif chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    except Exception as e:
        # Log the error without yielding it to the response
        print(f"Error in get_chatgpt_stream: {e}")


async def create_completions_chat(model_choice, messages, tool_choice):
    response = await aclient.chat.completions.create(model=model_choice,
    messages=messages,
    tools=tools,  # Lists tools for the model's usage
    tool_choice=tool_choice,  # "none" = message only, "auto" = message/tools, "required" = tools only
    parallel_tool_calls=True,  # Enables parallel tool calls. Set to true so the model can call multiple functions at once
    stream=True, # Enable streaming
    stream_options={"include_usage": True} # Enable token usage data in reponse. When true responses include prompt_tokens, completion_tokens, and total_tokens data.)
    )
    async for chunk in response:  # Ensure this yields chunks properly, needed for async generator
        yield chunk

# Parse chat history from FastAPI into required format for openai api
def parse_and_add_messages(data):
    cleaned_messages = []
    # Clean the most recent two messages to remove HTML tags
    for msg in data['message'][-2:]:
        cleaned_messages.append({
            "role": msg["role"],
            "content": re.sub(r'<.*?>', '', msg['content']).strip()
        })
    
    messages.extend(cleaned_messages)
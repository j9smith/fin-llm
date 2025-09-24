""" Handles requests for quantitative data by interacting with external APIs. Working towards engaging with 
financialmodelingprep_api_connector.py for API calls."""

from openai import AsyncOpenAI
from backend_app.Agents import BaseAgent
import os
import json 

system_prompt = f""
model_choice = "gpt-4o-mini"

file_path = os.path.join(os.path.dirname(__file__), "company_data_agent_tools.json")
with open(file_path, "r") as tools_file:
    tools = json.load(tools_file)

class CompanyDataAgent(BaseAgent):
    def __init__(self):
        # Can store persistent state variables here later down the line
        pass

    async def create_agent_response(self, prompt : str):
        return "Inform the user that company_data_agent was called successfully and that further functionality needs to be added to this agent. No further response is required."
        # try:
        #     aclient = AsyncOpenAI()
        #     messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

        #     response = await aclient.chat.completions.create(model=model_choice,
        #     messages=messages,
        #     tools=tools,  # Lists tools for the model's usage
        #     tool_choice="required",  # "none" = message only, "auto" = message/tools, "required" = tools only
        #     stream=True,
        #     parallel_tool_calls=True, 
        #     )

        #     return "response"

        # except Exception as e: 
        #     print(f"Exception occured in company_data_agent.py: {e}")
        #     return { f"error: {e}"}

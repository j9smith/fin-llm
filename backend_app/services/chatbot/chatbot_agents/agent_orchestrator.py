""" Handles all code pertaining to the orchestrating agent. Responsible for taking queries from the chatbot and directing them 
to appropriate agents to yield additional context for augmented generation. """

from openai import AsyncOpenAI
from backend_app.Agents import BaseAgent
from backend_app.services.data_access_layer.data_layer_agents.company_data_agent import CompanyDataAgent
import os
import json 
import asyncio

system_prompt = f"You're the orchestrating agent for a financial market research application. You will receive user prompts from the front-end chatbot agent and are to decide which agents to call on to fully satisfy the user request. You must call each agent once and only once. You may not make multiple calls to the same agent. Therefore, you must be sure to include all relevant context in your singular allowed agent call."
model_choice = "gpt-4o-mini"

file_path = os.path.join(os.path.dirname(__file__), "agent_orchestrator_tools.json")
with open(file_path, "r") as tools_file:
    tools = json.load(tools_file)

class AgentOrchestrator(BaseAgent):
    def __init__(self):
        self.company_data_agent = None

        self.available_agents = {
            "company_data_agent":  self.launch_company_data_agent
        }

    async def orchestrate_agents(self, prompt : str):
        """ The orchestration routine. Receives the user prompt along with any additional context specified by the 
        LLM (as described in the chat_logic/functions tools.json) and then calls on downstream agents using tailored
        generated prompts (as described in agent_orchestrator_tools.json). Returns a list.
        
        Parameters: 
        - prompt (str): specified by the chatbot agent, containing the user prompt and necessary additional context.
        
        Returns: 
        - results (list): a list of responses with contributions from each participating agent."""

        try:
            aclient = AsyncOpenAI()
            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

            response = await aclient.chat.completions.create(model=model_choice,
            messages=messages,
            tools=tools,  
            tool_choice="required",  # "required" = tools only 
            stream = True, # Streaming has to be enabled for parallel tool calls 
            parallel_tool_calls=True, 
            )

            agent_tasks = [] # List to hold the collection of agent calls to be performed
            accumulated_tool_calls = {} # Accumulator for the tool call chunks 

            async for chunk in response: 
                if not chunk.choices:
                    print(f"AgentOrchestrator token usage: {chunk.usage.total_tokens}")

                delta = chunk.choices[0].delta
                index = chunk.choices[0].index

                if index not in accumulated_tool_calls:
                    accumulated_tool_calls[index] = {
                        "function_name": None,
                        "arguments": ""
                    }

                accumulated_data = accumulated_tool_calls[index]

                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        if tool_call.function.name:
                            accumulated_data['function_name'] = tool_call.function.name
                        if tool_call.function.arguments:
                            accumulated_data['arguments'] += tool_call.function.arguments

                        try:
                            parsed_args = json.loads(accumulated_data['arguments'])
                            instructions = parsed_args.get("instructions")
                            agent_name = accumulated_data['function_name']

                            agent_called = self.available_agents.get(agent_name)
                            if agent_called:
                                print(f"AgentOrchestrator: calling on {agent_name} with prompt: '{instructions}'")
                                if asyncio.iscoroutinefunction(agent_called):
                                    agent_tasks.append(agent_called(parsed_args))
                                else:
                                    agent_tasks.append(asyncio.to_thread(agent_called, parsed_args))
                                del accumulated_tool_calls[index]
                            else: 
                                error_message = f"Agent {agent_name} does not exist."
                                print(f"Error in agent_orchestrator.py: {error_message}")
                                return {"error": error_message}
                        except json.JSONDecodeError:
                            pass      
            if agent_tasks: 
                results = await asyncio.gather(*agent_tasks, return_exceptions=True)
                return results
            else: 
                print("agent_orchestrator.py: no agent calls found.")
                return "No agents were called."

        except Exception as e: 
            print(f"Exception occured in agent_orchestrator.py: {e}")
            return { f"error: {e}"}
    
    def get_company_data_agent(self): 
        """ Getter method for the company data agent object. 

        We're using lazy initalisation so the object is only created when it is needed.
         
        This will initialise the Company Data Agent. Change to async if we use async routines in initialisation.
        
        Returns: 
        - CompanyDataAgent object"""
        
        if not self.company_data_agent: 
            self.company_data_agent = CompanyDataAgent()
        return self.company_data_agent
    
    async def launch_company_data_agent(self, arguments : dict):
        """ Launches the CompanyDataAgent which is responsible for handling quantitative API requests.

        Linked to 'company_data_agent' in agent_orchestrator_tools.json. 
        
        Parameters: 
        - arguments (dict): a dictionary containing the parameters specified in agent_orchestrator_tools.py.
        
        Returns: 
        - a response (currently formatted as string)"""

        instructions = arguments.get("instructions")

        company_data_agent = self.get_company_data_agent() # Lazy intialisation
        agent_response = await company_data_agent.create_agent_response(instructions)
        return agent_response
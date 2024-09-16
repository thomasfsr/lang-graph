from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

from tools import RandomTool, HistTool
from dotenv import load_dotenv
import functools
import os

load_dotenv()
key = os.getenv('openai_key')
gpt4mini = "gpt-4o-mini"
gpt3turbo = "gpt-3.5-turbo"

llm = ChatOpenAI(api_key=key, model=gpt3turbo, temperature=0)

class RouteSchema(BaseModel):
    next: str = Field(description="The name of the next worker or 'FINISH'.")

class Nodes:
    def __init__(self):
        self.llm = llm

    def supervisor(self):
        members = ["Lotto_Manager", "Coder"]
        system_prompt = (
            "You are a supervisor tasked with managing a conversation between the"
            " following workers:  {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. When finished,"
            " respond with FINISH."
        )
        # Our team supervisor is an LLM node. It just picks the next agent to process
        # and decides when the work is completed
        options = ["FINISH"] + members
        # Using openai function calling can make output parsing easier for us
        function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {"title": "routeSchema",
                            "type": "object",
                            "properties": {
                                            "next": {
                                                    "title": "Next",
                                                    "anyOf": [{"enum": options}],
                                                    }
                                        },
                            "required": ["next"],
                        },
        }
        supervisor_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}",
                ),
            ]
        ).partial(options=str(options), members=", ".join(members))


        return (
            supervisor_prompt
            | self.llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )

    def create_agent(self, llm: ChatOpenAI, tools:list, system_prompt: str):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_tools_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools
                                #  ,verbose=True,
                                )
        return executor

    def agent_node(self, state, agent, name):
        result = agent.invoke(state)
        return {"messages": [HumanMessage(content=result["output"], name=name)]}
    
    def lotto_node(self):
        lotto_agent = self.create_agent(self.llm, tools =[RandomTool()], system_prompt= "You are a senior lotto manager. you run the lotto and get random numbers.")
        lotto_node = functools.partial(self.agent_node, agent=lotto_agent, name= 'Lotto_Manager')
        return lotto_node

    def coder_node(self):
        coder_agent = self.create_agent(self.llm, tools =[HistTool()], system_prompt= "You may generate as list and a number of bins for the tool to plot a histogram.")
        coder_node = functools.partial(self.agent_node, agent=coder_agent, name= 'Coder')
        return coder_node 
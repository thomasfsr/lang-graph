from graph import Workflow

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

wf = Workflow()

resp = wf.response("""Get 30 random lotto numbers and plot them in a histogram with 5 bins""")
# print(resp['messages'][-2].content)
print(resp)


# from dotenv import load_dotenv
# import functools
# import os

# load_dotenv()
# key = os.getenv('GROQ_API_KEY')

# llm = ChatGroq(api_key=key, temperature=0)
# resp = llm.invoke(input = [HumanMessage('qual a capital de minas gerais?')])

# print(resp.content)

# print(resp.type)
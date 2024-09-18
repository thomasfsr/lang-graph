from graph import Workflow

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
3




wf = Workflow()

resp = wf.response("""Get 5 random lotto numbers""")
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
from graph import Workflow

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

wf = Workflow()

resp = wf.response("""Get 5 random lotto numbers""")

print(resp)


# from dotenv import load_dotenv
# import functools
# import os

# load_dotenv()
# key = os.getenv('GROQ_API_KEY')

# llm = ChatGroq(api_key=key, temperature=0)
# print(llm.invoke(input = 'qual a capital de minas gerais?'))
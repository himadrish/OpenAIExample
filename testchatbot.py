import getpass
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.messages import AIMessage

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "YOUR SANGSMITH KEY GOES HERE"

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("YOUR OPENAI KEY GOES HERE")


chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
response = chat.invoke(
  [
    HumanMessage(content="Hi! I'm Himadrish"),
    AIMessage(content="Hello Himadrish! How can I help you today?"),
    HumanMessage(content="What is my first name?"),
   ]
  
  )
print(response.content)
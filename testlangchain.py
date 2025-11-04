import getpass
import os

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from langchain_core.prompts import ChatPromptTemplate

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("YOUR OPENAPI KEY GOES HERE")

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

#set1 example
#response = chat.invoke([HumanMessage(content="Hi buddy, how are you?")])
#print(response.content)

#set2 example
system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

prompt = prompt_template.invoke({"language": "Bengali", "text": "Good morning!"})

response = chat.invoke(prompt)
print(response.content)

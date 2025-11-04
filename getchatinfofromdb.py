import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import Annotated, TypedDict
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph


os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "YOUR LANGSMITH KEY GOES HERE"

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = "YOUR OPENAPI KEY GOES HERE"

#LLM model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

#Class declaration
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

system_message = """
Given an input question, create a syntactically correct {dialect} query to
run to help find the answer. Pay attention to limit your query to
at most {top_k} results.

Never query for all the columns from a specific table, only ask for a the
few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema
description. 

Only use the following tables:
{table_info}
"""

#Part 1 - query builder

user_prompt = "Question: {input}"

query_prompt_template = ChatPromptTemplate(
    [("system", system_message), ("user", user_prompt)]
)

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

def write_query(state: State):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": "DRIVER={ODBC Driver 17 for SQL Server};SERVER=TUKAI\\MSSQLSERVER01;DATABASE=EasyDate;Trusted_Connection=yes;",
            "top_k": 10,
            "table_info": "dbo.Users",
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

response_query = write_query({"question": "How many Employees are there?"})

print(response_query)


#Part 2 - Execute query 

def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=query_prompt_template.dialect)
    QueryResponse = execute_query_tool.invoke(state["query"])
    print(QueryResponse)                                         
    return {"result": QueryResponse}

def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f"Question: {state['question']}\n"
        f"SQL Query: {state['query']}\n"
        f"SQL Result: {state['result']}"
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

#Final step using LangGraph

graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()


for step in graph.stream(
    {"question": "How many employees are there?"}, stream_mode="updates"
):
    print(step)
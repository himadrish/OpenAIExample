import os
import pyodbc

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "YOUR LANGSMITH KEY GOES HERE"

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = "YOUR OPENAPI KEY GOES HERE"

#from langchain_community.utilities import SQLDatabase

#conn_str = "mssql+pyodbc:///?odbc_connect=DRIVER={SQL Server};SERVER=TUKAI\MSSQLSERVER01;DATABASE=EASY_DATE;Trusted_Connection=yes;"
#db = SQLDatabase.from_uri(conn_str)

#print(db.dialect)
#print(db.get_usable_table_names())
#response = db.run("SELECT * FROM Users LIMIT 10;")
#print(response.content)

#print(pyodbc.drivers())

#CASE-1 where SQL credential (UserId, and Password) is required to be used
#conn = pyodbc.connect(
#    "DRIVER={ODBC Driver 17 for SQL Server};"
#    "SERVER=TUKAI\MSSQLSERVER01;"
#    "DATABASE=EasyDate;"
#    "UID=Test;"
#    "PWD=Test4321!;"
#    "TrustServerCertificate=yes;"
#)

#CASE-2 where windows credential is being use
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=TUKAI\MSSQLSERVER01;"
    "DATABASE=EasyDate;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.execute("SELECT TOP 5 * FROM dbo.Users")
for row in cursor:
    print(row)
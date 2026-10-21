from langchain_core.prompts import ChatPromptTemplate 
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser 

prompt = ChatPromptTemplate.from_template("Responde de forma clara y concisa: {pregunta}")
llm = ChatOllama(model="llama3.2", temperature=0.3)
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"pregunta": "¿Qué es un vector embedding?"}))
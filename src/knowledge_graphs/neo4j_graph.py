import os

from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from langchain_community.llms.ollama import Ollama
from langchain_experimental.graph_transformers import LLMGraphTransformer

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "neo4j123456"

"""
%pip install --upgrade --quiet  langchain langchain-community langchain-openai langchain-experimental neo4j
https://python.langchain.com/docs/use_cases/graph/constructing/
https://neo4j.com/docs/operations-manual/current/installation/
"""


graph = Neo4jGraph()
Ollama(model="llama3")
llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")
llm = ChatOllama(model="llama3")

llm_transformer = LLMGraphTransformer(llm=llm)


from langchain_core.documents import Document

text = """
Marie Curie, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris.
"""
documents = [Document(page_content=text)]
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relationships:{graph_documents[0].relationships}")

'''
请注意，由于我们使用的是 LLM，因此图构建过程是不确定的。因此，每次执行时您可能会得到略有不同的结果。

此外，您还可以根据您的要求灵活地定义特定类型的节点和关系以进行提取。
'''
# llm_transformer_filtered = LLMGraphTransformer(
#     llm=llm,
#     allowed_nodes=["Person", "Country", "Organization"],
#     allowed_relationships=["NATIONALITY", "LOCATED_IN", "WORKED_AT", "SPOUSE"],
# )
# graph_documents_filtered = llm_transformer_filtered.convert_to_graph_documents(
#     documents
# )
# print(f"Nodes:{graph_documents_filtered[0].nodes}")
# print(f"Relationships:{graph_documents_filtered[0].relationships}")

# graph.add_graph_documents(graph_documents_filtered)
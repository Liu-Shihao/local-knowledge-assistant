import os
from typing import Optional

from langchain import hub
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.qa_rag import documents_loaders

'''
1.Load
2.Split
3.Store(Embedding & Vector)
4.Retrieval & generation
'''
faiss_folder_path: str = "./faiss_index"
text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
embeddings = OllamaEmbeddings(model="llama2")
llm = ChatOllama(model="llama2")
prompt = hub.pull("rlm/rag-prompt")
db = FAISS.load_local(faiss_folder_path, embeddings,allow_dangerous_deserialization=True)



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
        )


def insert(source):
    docs = documents_loaders.load_web(source).load()
    all_splits = text_splitter.split_documents(docs)
    new_db = FAISS.from_documents(all_splits, embeddings)
    db.merge_from(new_db)
    db.save_local("faiss_index")
    print("Vector database saved to local file")
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
def ask(prompt):

    result = rag_chain.invoke(prompt)
    for chunk in result:
        print(chunk, end="", flush=True)
    return result

# class QAChatbot:
#     faiss_folder_path: str = "./faiss_index"
#     def __init__(self):
#         self.embeddings = OllamaEmbeddings(model="llama2")
#         self.llm = ChatOllama(model="llama2")
#         self.prompt = hub.pull("rlm/rag-prompt")
#         if os.path.exists(self.faiss_folder_path):
#             self.db = FAISS.load_local(self.faiss_folder_path, self.embeddings,allow_dangerous_deserialization=True)
#             print("Load the local vector database successfully.")
#         else:
#             self.db = FAISS.from_texts("init", self.embeddings)
#             print("Init vector database successfully.")
#         self.retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#         self.rag_chain = (
#                 {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
#                 | self.prompt
#                 | self.llm
#                 | StrOutputParser()
#         )
#
#     # 打印出所有文档内容的字符串表示，并且每个文档内容之间有两个换行符分隔开。
#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)
#
#     def insert(self,source):
#         docs = documents_loaders.load_web(source).load()
#
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000, chunk_overlap=200, add_start_index=True
#         )
#
#         all_splits = text_splitter.split_documents(docs)
#
#         new_db = FAISS.from_documents(all_splits, self.embeddings)
#         self.db.merge_from(new_db)
#         self.retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#         self.rag_chain = (
#                 {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
#                 | self.prompt
#                 | self.llm
#                 | StrOutputParser()
#         )
#
#     def ask(self,prompt):
#
#         result = self.rag_chain.invoke(prompt)
#         for chunk in result:
#             print(chunk, end="", flush=True)
#         return result

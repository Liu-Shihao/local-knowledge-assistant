import os
from pprint import pprint
from typing import Optional

from langchain import hub
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel
from src.qa_rag import documents_loaders

'''
1.Load
2.Split
3.Store(Embedding & Vector)
4.Retrieval & generation
'''

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class LocalFaissDb:
    faiss_folder_path: str = "faiss_index"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    embeddings = OllamaEmbeddings(model="llama2")
    llm = ChatOllama(model="llama2")
    prompt = hub.pull("rlm/rag-prompt")

    def __init__(self):
        if os.path.exists(self.faiss_folder_path):
            self.db = FAISS.load_local(self.faiss_folder_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.db = FAISS.from_texts(["foo"], self.embeddings)

        self.retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

localFaissDb = LocalFaissDb()

def insertWebContent(urls):

    docs = documents_loaders.load_web(urls).load()
    all_splits = localFaissDb.text_splitter.split_documents(docs)
    new_db = FAISS.from_documents(all_splits, localFaissDb.embeddings)
    localFaissDb.db.merge_from(new_db)
    localFaissDb.db.save_local(localFaissDb.faiss_folder_path)
    print("Data insert successful and Vector saved to local file.")

def insertImg(img):
    pass
def insertFile(file):
    pass


def ask(prompt):
    # Chain without sources
    # rag_chain = (
    #         {"context": localFaissDb.retriever | format_docs, "question": RunnablePassthrough()}
    #         | localFaissDb.prompt
    #         | localFaissDb.llm
    #         | StrOutputParser()
    # )
    # result = rag_chain.invoke(prompt)

    # Adding sources
    rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | localFaissDb.prompt
            | localFaissDb.llm
            | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": localFaissDb.retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    result = rag_chain_with_source.invoke(prompt)
    pprint(result)
    # for chunk in result:
    #     print(chunk, end="", flush=True)
    return result

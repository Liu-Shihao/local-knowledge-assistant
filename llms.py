import os
from pprint import pprint

from langchain import hub
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough


text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )

embeddings = OllamaEmbeddings(model="mistral")
mistral_chatbot = ChatOllama(model="mistral")
mistral_llm = Ollama(model="mistral")
llava_llm = Ollama(model="llava")
# template = hub.pull("rlm/rag-prompt")
# print(type(template))
# print(template)

TEMPLATE = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

human_message_template = HumanMessagePromptTemplate.from_template(TEMPLATE)

chat_template = ChatPromptTemplate.from_messages(
    messages=[
        human_message_template
    ]
)

faiss_folder_path: str = "data/faiss_index"
local_data_folder_path: str = "data/example_data"

if os.path.exists(faiss_folder_path):
    print("Loading local vector data...")
    db = FAISS.load_local(faiss_folder_path, embeddings, allow_dangerous_deserialization=True)
else:
    print("Initializes the vector database...")
    loader = DirectoryLoader(local_data_folder_path, glob="**/*.txt")
    docs = loader.load()
    all_splits = text_splitter.split_documents(docs)
    db = FAISS.from_documents(all_splits, embeddings)
    db.save_local(faiss_folder_path)

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# https://python.langchain.com/docs/use_cases/chatbots/quickstart/#prompt-templates
def chat(content):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chain = prompt | mistral_chatbot
    answer = chain.invoke(
        {
            "messages": [
                HumanMessage(content=content),
            ],
        }
    )
    return answer



def insert(data,type):
    print(type,":",data)
    if(type == "url"):
        docs = WebBaseLoader(data).load()
    all_splits = text_splitter.split_documents(docs)
    new_db = FAISS.from_documents(all_splits, embeddings)
    db.merge_from(new_db)
    db.save_local(faiss_folder_path)
    print("Data insert successful and Vector saved to local file.")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ask(q):
    print("prompt:",q)
    # rag_chain = (
    #         {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #         | template
    #         | llm
    #         | StrOutputParser()
    # )
    # result = rag_chain.invoke(prompt)

    rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | chat_template
            | mistral_llm
            | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    result = rag_chain_with_source.invoke(q)
    pprint(result)
    return result



# class LocalFaissDb:
#     faiss_folder_path: str = "data/faiss_index"
#     local_data_folder_path: str = "data/example_data"
#
#     def __init__(self):
#         if os.path.exists(self.faiss_folder_path):
#             print("Loading local vector data...")
#             self.db = FAISS.load_local(self.faiss_folder_path, self.embeddings, allow_dangerous_deserialization=True)
#         else:
#             print("Initializes the vector database...")
#             loader = DirectoryLoader(self.local_data_folder_path, glob="**/*.txt")
#             docs = loader.load()
#             all_splits = self.text_splitter.split_documents(docs)
#             self.db = FAISS.from_documents(all_splits, self.embeddings)
#             self.db.save_local(self.faiss_folder_path)
#         self.retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#
#     # 1. web url(html/jira/bitbucket)
#     # 2. file(txt/markdown)
#     # 3. image
#     def insert(self,data,type):
#         print(type,":",data)
#         if(type == "url"):
#             docs = WebBaseLoader(data).load()
#         all_splits = text_splitter.split_documents(docs)
#         new_db = FAISS.from_documents(all_splits, self.embeddings)
#         self.db.merge_from(new_db)
#         self.db.save_local(self.faiss_folder_path)
#         print("Data insert successful and Vector saved to local file.")
#
# faiss_vector = LocalFaissDb()
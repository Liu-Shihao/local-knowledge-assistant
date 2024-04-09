from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores.faiss import FAISS

embeddings = OllamaEmbeddings(model="llama2")
if __name__ == '__main__':
    allow_dangerous_deserialization = True
    new_db = FAISS.load_local("faiss_index", embeddings)
from langchain_community.document_loaders.web_base import WebBaseLoader



# https://python.langchain.com/docs/integrations/document_loaders/web_base/#loading-multiple-webpages
def load_web(url):
    return WebBaseLoader(url)
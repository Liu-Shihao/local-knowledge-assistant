from pprint import pprint

from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.web_base import WebBaseLoader
'''
https://python.langchain.com/docs/modules/data_connection/document_loaders/
https://python.langchain.com/docs/integrations/document_loaders/web_base/
https://python.langchain.com/docs/modules/data_connection/document_loaders/json/
'''
# 加载TXT格式文件
from langchain_community.document_loaders import TextLoader

loader = TextLoader("../README.md")
print(loader.load())
# 加载Markdown文件 # !pip install unstructured > /dev/null   pip install markdown
from langchain_community.document_loaders import UnstructuredMarkdownLoader
markdown_path = "../README.md"
loader = UnstructuredMarkdownLoader(markdown_path)
print(loader.load())

# webBaseLoader = WebBaseLoader("https://www.espn.com/")
# # webBaseLoader = WebBaseLoader(["https://www.espn.com/", "https://google.com"])
# data = webBaseLoader.load()
# print(data)
#
#
# from langchain_community.document_loaders import PyPDFLoader
#
# loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
# pages = loader.load_and_split()
# print(pages[0])
#
# # pip install rapidocr-onnxruntime 提取图像为文本
# loader = PyPDFLoader("https://arxiv.org/pdf/2103.15348.pdf", extract_images=True)
# pages = loader.load()
# pages[4].page_content

# pip install jq 加载JSON文件
#
# loader = JSONLoader(
#     file_path='../example_data/facebook_chat.json',
#     jq_schema='.messages[].content',
#     text_content=False)
#
# data = loader.load()
# pprint(data)

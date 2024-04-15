from src import extract_hyperlink

# 测试示例
text_with_hyperlink = 'Check out this link: https://python.langchain.com/docs/use_cases/question_answering/quickstart/'
text_without_hyperlink = 'This is just plain text'

print('Text contains hyperlink:', extract_hyperlink.contains_hyperlink(text_with_hyperlink))
print('Text contains hyperlink:', extract_hyperlink.contains_hyperlink(text_without_hyperlink))

print('Text is a hyperlink:', extract_hyperlink.is_hyperlink(text_with_hyperlink))
print('Text is a hyperlink:', extract_hyperlink.is_hyperlink(text_without_hyperlink))


text_with_hyperlinks = 'Check out these links: https://github.com/xiaolai/everyone-can-use-english and https://techcommunity.microsoft.com/t5/ai-ai-platform-blog/raft-a-new-way-to-teach-llms-to-be-better-at-rag/ba-p/4084674'
hyperlinks = extract_hyperlink.extract_hyperlinks(text_with_hyperlinks)
print('Extracted hyperlinks:', hyperlinks)

'''
Text contains hyperlink: True
Text contains hyperlink: False
Text is a hyperlink: False
Text is a hyperlink: False
Extracted hyperlinks: ['https://github.com/xiaolai/everyone-can-use-english', 'https://techcommunity.microsoft.com/t5/ai-ai-platform-blog/raft-a-new-way-to-teach-llms-to-be-better-at-rag/ba-p/4084674']

'''
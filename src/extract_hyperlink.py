import re

def contains_hyperlink(text):
    # 定义超链接的正则表达式模式
    hyperlink_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

    # 使用正则表达式查找文本中是否包含超链接
    return bool(re.search(hyperlink_pattern, text))

def is_hyperlink(text):
    # 定义超链接的正则表达式模式
    hyperlink_pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    # 使用正则表达式检查文本是否是一个超链接
    return bool(re.match(hyperlink_pattern, text))


def extract_hyperlinks(text):
    hyperlink_pattern = r'https?://\S+'
    # 使用正则表达式查找文本中的所有超链接
    hyperlinks = [match.group(0) for match in re.finditer(hyperlink_pattern, text)]

    return hyperlinks
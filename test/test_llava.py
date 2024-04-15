from PIL import Image

from langchain_community.llms.ollama import Ollama

from src.convert_imgs import convert_to_base64
"""

❯ ollama run llava
>>> What is the dollar based gross retention rate? /Users/liushihao/PycharmProjects/local-knowledge-assistant/data/example_data/ol
... lama_example_img.jpg
Added image '/Users/liushihao/PycharmProjects/local-knowledge-assistant/data/example_data/ollama_example_img.jpg'
 The dollar based gross retention rate in the image is 100%. 
 
❯ ollama run bakllava 
>>> What is the dollar based gross retention rate? /Users/liushihao/PycharmProjects/local-knowledge-assistant/data/example_data/ol
... lama_example_img.jpg
Added image '/Users/liushihao/PycharmProjects/local-knowledge-assistant/data/example_data/ollama_example_img.jpg'
90%

"""
if __name__ == '__main__':
    # llava_llm = Ollama(model="llava")
    bakllava_llm = Ollama(model="bakllava")

    file_path = "/Users/liushihao/PycharmProjects/local-knowledge-assistant/data/example_data/ollama_example_img.jpg"
    pil_image = Image.open(file_path)
    image_b64 = convert_to_base64(pil_image)

    llm_with_image_context = bakllava_llm.bind(images=[image_b64])
    prompt1 = "What is the dollar based gross retention rate:"
    prompt2 = "What is the dollar based net retention rate:"
    result = llm_with_image_context.invoke(prompt2)
    print(result)

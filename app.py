import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

import llms
from llms import insert
from src import extract_hyperlink

app = Flask(__name__)

# 保存图片的文件夹路径
UPLOAD_FOLDER = 'data/uploads'
# 允许上传的图片文件类型
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 允许上传的文件类型
ALLOWED_FILE_EXTENSIONS = {'txt', 'pdf', 'xls', 'xlsx'}
# 支持的媒体类型
SUPPORTED_MEDIA_TYPES = ['application/json', 'multipart/form-data']

# 设置上传文件夹
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查文件扩展名是否在允许的范围内
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS
def allowed_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def save_disk(file):
    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_path)
    print(file.filename,"File saved successfully")

# TODO 加入上下文、对话历史
@app.route('/chat', methods=['GET'])
def chat():
    question = request.form.get('q', '')

    answer = llms.chat(question)
    print("question:",question)
    print("answer:", answer)

    return jsonify({'question': question,
                    'answer': answer.content})

# 定义搜索的路由
@app.route('/ask', methods=['GET'])
def ask():

    q = request.form.get('q', '')

    if extract_hyperlink.is_hyperlink(q) or extract_hyperlink.contains_hyperlink(q):
        hyperlinks = extract_hyperlink.extract_hyperlinks(q)
        # 插入Web页面内容
        insert(hyperlinks,"url")
        return jsonify({'msg': 'Load complete, Please Ask.'})
    else:
        answer = llms.ask(q)
        return jsonify({'question': answer['question'],
                        'answer': answer['answer'],
                        'sources': answer['context'][0].metadata['source']
                        })

    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_img(file.filename):
            save_disk(file)
            # TODO Img
            return jsonify({'msg': 'Image saved and search request received successfully'})
        elif file and allowed_file(file.filename):
            save_disk(file)
            # TODO File
            return jsonify({'msg': 'File saved and search request received successfully'})
        else:
            return jsonify({'error': 'Invalid file'})

if __name__ == '__main__':
    app.run(debug=True,
            port=8080)

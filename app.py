import atexit
import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from src.qa_rag import web_qa_chat

from src.utils import extract_hyperlink

app = Flask(__name__)

# 保存图片的文件夹路径
UPLOAD_FOLDER = './uploads'
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



# 定义搜索的路由
@app.route('/search', methods=['GET'])
def search():

    prompt = request.form.get('q', '')

    if extract_hyperlink.is_hyperlink(prompt) or extract_hyperlink.contains_hyperlink(prompt):
        hyperlinks = extract_hyperlink.extract_hyperlinks(prompt)
        web_qa_chat.insert(hyperlinks)
        return jsonify({'msg': 'Load complete, Please Ask!'})
    else:
        answer = web_qa_chat.ask(prompt)
        return jsonify({'answer': answer})

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

# 在应用上下文销毁时保存向量数据库到本地
@app.teardown_appcontext
def save_database_on_shutdown(exception=None):
    web_qa_chat.db.save_local("faiss_index")
    print("Vector database saved to local file")

# 注册服务终止时执行的方法
def save_database_on_exit():
    web_qa_chat.db.save_local("faiss_index")
    print("Vector database saved to local file")

# 在程序终止时执行
atexit.register(save_database_on_exit)

if __name__ == '__main__':
    app.run(debug=True,
            port=8080)

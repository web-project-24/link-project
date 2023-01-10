from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.j5o0d68.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)
from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['POST'])
def save_diary():

    post_list = list(db.links.find({}, {'_id': False}))
    id = len(post_list) + 1
    title = request.form['title']
    url = request.form['url']
    tag = request.form['tag']
    author = request.form['author']
    # 파일 저장을 위한 부분
    image = request.files["file"]

    # 파일 확장자
    extension = image.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    image.save(save_to)

    doc = {
        'id': id,
        'title': title,
        'url': url,
        'tag': tag,
        'author': author,
        'image': image,
    }

    db.links.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


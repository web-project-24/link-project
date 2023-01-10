from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient

from datetime import datetime
# DB 환경설정
client = MongoClient('mongodb+srv://team24:2424@cluster0.ypbmrjf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#업로드
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

# 링크 전체 조회
@app.route("/api/link", methods=["GET"])
def link_list_get():
    _linklist = list(db.links.find({}, {'_id': False}))

    return jsonify({'linklist': _linklist})

# 링크 생성 create
@app.route("/api/link", methods=["POST"])
def link_post():
    # id 값 만들기
    all_list = list(db.links.find({}, {'_id': False}))
    id = len(all_list) + 1

    title = request.form['title']
    url = request.form['url']
    tag = request.form['tag']
    author = request.form['author']
    image = request.form['image']

    doc = {
        'id': id,
        'title': title,
        'url': url,
        'tag': tag,
        'author': author,
        'image': image
    }
    db.links.insert_one(doc)

    return jsonify({'msg': '링크 등록 완료!'})

# 링크 수정 update
@app.route("/api/link/<int:id>", methods=["PUT"])
def link_put(id):
    _title = request.form['title']
    print(_title)

    return jsonify({'msg': '링크 수정 완료!', 'path': id})

# 링크 삭제 delete
@app.route("/api/link/<int:id>", methods=["DELETE"])
def link_delete(id):
    print(id)

    return jsonify({'msg': '링크 삭제 완료!', 'path': id})


if __name__ == '__main__':
    app.run(debug=True)

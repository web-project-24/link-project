from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient

# DB 환경설정
client = MongoClient('mongodb+srv://team24:2424@cluster0.ypbmrjf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# 링크 전체 조회
@app.route("/api/link", methods=["GET"])
def link_list_get():
    _linklist = list(db.links.find({}, {'_id': False}))

    return jsonify({'linklist': _linklist})


# 링크 생성
@app.route("/api/link", methods=["POST"])
def link_post():
    title = request.form['title']
    url = request.form['url']
    tag = request.form['tag']
    author = request.form['author']
    image = request.form['image']

    count = list(db.links.find({}, {'_id': False}))
    id = len(count) + 1

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

# 링크 수정
@app.route("/api/link/<int:id>", methods=["PUT"])
def link_put(id):

    title = request.form['title']
    url = request.form['url']
    tag = request.form['tag']
    author = request.form['author']
    image = request.form['image']

    new_doc = {
        'id': id,
        'title': title,
        'url': url,
        'tag': tag,
        'author': author,
        'image': image
    }

    db.links.update_one({'id':int(id)},{'$set': new_doc})

    return jsonify({'msg': '링크 수정 완료!', 'path': id})


# 링크 삭제
@app.route("/api/link/<int:id>", methods=["DELETE"])
def link_delete(id):
    db.links.delete_one({'id': id})

    return jsonify({'msg': '링크 삭제 완료!', 'path': id})


if __name__ == '__main__':
    app.run(debug=True)

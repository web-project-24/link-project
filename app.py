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
    _linklist = request.args.get('link')

    return jsonify({'linklist': _linklist})

# 링크 생성
@app.route("/api/link", methods=["POST"])
def link_post():
    _title = request.form['title']

    return jsonify({'msg': '링크 등록 완료!'})

# 링크 수정
@app.route("/api/link/<int:id>", methods=["PUT"])
def link_put(id):
    _title = request.form['title']

    return jsonify({'msg': '링크 수정 완료!', 'path': id})

# 링크 삭제
@app.route("/api/link/<int:id>", methods=["DELETE"])
def link_delete(id):


    return jsonify({'msg': '링크 삭제 완료!', 'path': id})


if __name__ == '__main__':
    app.run(debug=True)

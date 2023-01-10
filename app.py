from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient

from datetime import datetime
# DB 환경설정
client = MongoClient('mongodb+srv://team24:2424@cluster0.ypbmrjf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # UTF-인코딩

@app.route('/')
def home():
    return render_template('index.html')

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
    # 파일 저장을 위한 부분
    image = request.files['image']
    image_path = save_file(image)

    doc = {
        'id': id,
        'title': title,
        'url': url,
        'tag': tag,
        'author': author,
        'image': image_path
    }
    db.links.insert_one(doc)

    return jsonify({'msg': '링크 등록 완료!'}), 201


# 링크 수정 update
@app.route("/api/link/<int:id>", methods=["PUT"])
def link_put(id):
    # id가 유효한지 확인
    exist = db.links.find({'id': int(id)}, {'_id': False})
    # 유효하지 않는 경우
    if len(list(exist)) == 0 :
        return jsonify({'msg': '존재하지 않는 링크 ID입니다. 다시 확인해주세요.'}), 404
    # id가 유효한 경우
    else:
        title = request.form['title']
        url = request.form['url']
        tag = request.form['tag']
        author = request.form['author']
        # 파일 저장을 위한 부분
        image = request.files['image']
        image_path = save_file(image)

        new_doc = {
            'id': id,
            'title': title,
            'url': url,
            'tag': tag,
            'author': author,
            'image': image_path
        }
        db.links.update_one({'id': int(id) }, {'$set': new_doc })

        return jsonify({'msg': '링크 수정 완료!'}), 201


# 파일 업로드
def save_file(image):
    # 파일 확장자 분리
    extension = image.filename.split('.')[-1]
    # 파일 이름 형식
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'
    save_to = f'static/img/{filename}.{extension}'
    # 파일 로컬 static/img 디렉토리 저장
    image.save(save_to)

    file_fullname = f'{filename}.{extension}'

    return file_fullname

# 링크 삭제 delete
@app.route("/api/link/<int:id>", methods=["DELETE"])
def link_delete(id):
    # id가 유효한지 확인
    exist_id = db.links.find({'id': id}, {'_id': False})
    # 유효하지 않는 경우
    if len(list(exist_id)) == 0:
        return jsonify({'msg': '존재하지 않은 링크 ID입니다. 다시 확인해주세요.'}), 404
    # id가 유효한 경우
    db.links.delete_one({'id': id})

    return jsonify({'msg': '링크 삭제 완료!'}), 200


if __name__ == '__main__':
    app.run(debug=True)

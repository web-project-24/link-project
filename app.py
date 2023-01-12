from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import boto3, os
from pymongo import MongoClient, ReturnDocument

from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # UTF-인코딩
load_dotenv() # 환경변수 불러오기

# DB 환경설정
client = MongoClient(os.getenv('DB_URL'))
db = client.dbsparta

# AWS s3 설정
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)

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
    title = request.form['title']
    url = request.form['url']
    tag = request.form['tag']
    author = request.form['author']
    # 파일 저장을 위한 부분
    image = request.files['image']
    image_path = save_file(image)

    doc = {
        'id': create_index('id'),
        'title': title,
        'url': url,
        'tag': tag,
        'author': author,
        'image': image_path
    }
    db.links.insert_one(doc)

    return jsonify({'msg': '링크 등록 완료!'}), 201

# 인덱스 생성
def create_index(name):
    index_doc = db.counters.find_one_and_update(
        {'_id': name },
        {'$inc': {'sequence_value': 1}},
        return_document=ReturnDocument.AFTER
    )
    return index_doc['sequence_value']


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

        # 수청 요청 받은 파일이 없으면, 기존 URL 그대로 저장
        if image.filename != '':
            new_image = save_file(image)
        else:
            pre_link = list(db.links.find({'id': id}, {'_id': False}))
            new_image = pre_link[0]['image']

        new_doc = {
            'id': id,
            'title': title,
            'url': url,
            'tag': tag,
            'author': author,
            'image': new_image
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
    file_fullname = f'{filename}.{extension}'

    try:
        # S3 - Upload a new file
        bucket = os.getenv("AWS_BUCKET_NAME")
        s3.put_object(Key=file_fullname, Bucket=bucket, Body=image)

        path = os.getenv("AWS_DOMAIN")
        url = f'{path}/{file_fullname}'

        return url

    except Exception as e:
        return e


# 링크 삭제 delete
@app.route("/api/link/<int:id>", methods=["DELETE"])
def link_delete(id):
    # id가 유효한지 확인
    exist_id = list(db.links.find({'id': id}, {'_id': False}))
    # 유효하지 않는 경우
    if len(list(exist_id)) == 0:
        return jsonify({'msg': '존재하지 않은 링크 ID입니다. 다시 확인해주세요.'}), 404
    # id가 유효한 경우
    # s3 파일 삭제
    pre_image = exist_id[0]['image']
    delete_file(pre_image)
    # DB 삭제
    db.links.delete_one({'id': id})

    return jsonify({'msg': '링크 삭제 완료!'}), 200

# S3 삭제
def delete_file(image_path):

    bucket = os.getenv("AWS_BUCKET_NAME")
    file_key = image_path.split('/')[-1]

    try:
        response = s3.delete_object(
            Bucket=bucket,
            Key=file_key,
        )
        print(response)
        return

    except Exception as e:
        return e


if __name__ == '__main__':
    app.run(debug=True)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://team24:2424@cluster0.ypbmrjf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

doc = {
    'id' :'1',
    'title' :'devfolio',
    'url' :'https://devfolio.kr/' ,
    'tag' :'개발',
    'author' :'이재욱',
    'image' :'https://devfolio.kr/static/media/logo.c08ba2de.png'
}

db.links.insert_one(doc)
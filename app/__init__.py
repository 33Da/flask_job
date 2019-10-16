import pymongo
from flask import Flask
app = Flask(__name__)

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
#库名
mdb = client['myposts']
# 获取数据库里存放数据的表名
db = mdb['posts']

app.debug=True
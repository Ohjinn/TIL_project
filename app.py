import requests
import time
import sys
import urllib
import jwt
import hashlib
import bCrawling
from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta



class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())
SECRET_KEY = 'SPARTA'


client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbTil

"""
주기적 실행을 위한 flask-apscheduler 라이브러리 (https://viniciuschiele.github.io/flask-apscheduler/rst/usage.html)
"""
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id='autocraw', seconds=900, misfire_grace_time=900)
def autocraw():
    bCrawling.titlecrawling()


@scheduler.task('interval', id='autoPiccraw', seconds=3600, misfire_grace_time=900)
def autopiccraw():
    bCrawling.getpic()


@app.route('/')
def index():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
        status = (user_info != "")
        return render_template('index.html', user_info=user_info, status=status)
    except jwt.ExpiredSignatureError:
        return render_template('index.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('index.html', msg="로그인 정보가 존재하지 않습니다.")


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.userInfo.find_one({'id': username_receive, 'pw': pw_hash})
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    name_receive = request.form['name_give']
    birth_receive = request.form['birth_give']
    url_receive = request.form['url_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": username_receive,
        "pw": password_hash,
        "name": name_receive,
        "birth": birth_receive,
        "url": url_receive,
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": ""
    }
    db.userInfo.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.userInfo.find_one({"id": username_receive}))
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sorted', methods=['GET'])
def sorting():
    news = list(db.userStack.find({}, {'_id': False}))
    news.reverse()
    velogcards = []
    tistorycards = []
    for x in news:
        tempname = x['name']
        tempurl = db.userInfo.find_one({'name': tempname}, {'_id': False})['url']
        if 'velog' in tempurl:
            velogcards.append(db.userInfo.find_one({'name': tempname}, {'_id': False}))
        elif 'tistory' in tempurl:
            tistorycards.append(db.userInfo.find_one({'name': tempname}, {'_id': False}))

    return jsonify({'velogcards': velogcards, 'tistorycards': tistorycards})


# 검색
@app.route('/search', methods=['GET'])
def search():
    txt = request.args.get("txt")
    userdb = db.userInfo.find_one({'name': txt}, {'_id': False})
    return jsonify(userdb)


# 리뷰
@app.route('/review', methods=['POST'])
def modalreview():
    user_receive = request.form['user_give']
    review_receive = request.form['review_give']

    doc = {
        'user': user_receive,
        'review': review_receive
    }
    db.tilreview.insert_one(doc)

    return jsonify({'msg': '저장되었습니다!'})


@app.route('/reviewTarget', methods=['POST'])
def modaltarget():
    target_receive = request.form['target_give']

    doc = {
        'target': target_receive
    }
    db.tilreview.insert_one(doc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
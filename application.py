import requests
import time
import sys
import urllib
import jwt
import os
import hashlib
import bCrawling
import boto3
from flask_cors import CORS
from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from flask_apscheduler import APScheduler
from flask_restx import Resource
from datetime import datetime, timedelta


class Config:
    SCHEDULER_API_ENABLED = True


application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})
application.config.from_object(Config())


# client = MongoClient("mongodb://localhost:27017/")
# SECRET_KEY = 'SPARTA'
# KAKAO_CODE = 'bc448c49046a3ad8a4f89959546084b3'
SECRET_KEY = os.environ.get("SECRET_KEY")
client = MongoClient(os.environ.get("MONGO_DB_PATH"))
KAKAO_CODE = os.environ.get("KAKAO_CODE")
db = client.dbTil

"""
주기적 실행을 위한 flask-apscheduler 라이브러리 (https://viniciuschiele.github.io/flask-apscheduler/rst/usage.html)
"""
scheduler = APScheduler()
scheduler.init_app(application)
scheduler.start()


@scheduler.task('interval', id='autocraw', seconds=900, misfire_grace_time=900)
def autocraw():
    bCrawling.titlecrawling()



@scheduler.task('interval', id='autoPiccraw', seconds=3600, misfire_grace_time=900)
def autopiccraw():
    bCrawling.getpic()


@application.route('/')
def index():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.userInfo.find_one({'id': payload['id']}, {"_id": False})
        status = (user_info is not None)
        return render_template('index.html', user_info=user_info, status=status)
    except jwt.ExpiredSignatureError:
        return render_template('index.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('index.html', msg="로그인 정보가 존재하지 않습니다.")


@application.route('/review/<keyword>')
def review(keyword):
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.userInfo.find_one({'id': payload['id']})
            status = (user_info is not None)
            return render_template('review.html', id=keyword, user_info=user_info, status=status)
        except jwt.ExpiredSignatureError:
            return render_template('review.html', msg="로그인 시간이 만료되었습니다.")
        except jwt.exceptions.DecodeError:
            return render_template('review.html', msg="로그인 정보가 존재하지 않습니다.")
    else:
        user_info = db.userInfo.find_one({'id': keyword})
        return render_template('review.html', id=keyword, user_info=user_info)


@application.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.userInfo.find_one({'id': username_receive, 'pw': pw_hash}, {"_id": False})
    if result is not None:
        user_info = db.userInfo.find_one({'id': username_receive}, {"_id": False})
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token, 'user_info' : user_info})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


def kakao_sign_in(infos):
    kakao_pw = 'kakao'
    kakao_id = infos['id']
    kakao_nickname = infos['properties']['nickname']
    kakao_password = hashlib.sha256(kakao_pw.encode('utf-8')).hexdigest()
    # 만약 회원이 아니면 회원가입
    if db.userInfo.find_one({'id': kakao_id, 'pw': kakao_password}) is None:
        doc = {
            'id': kakao_id,
            'pw': kakao_password,
            'name': kakao_nickname
        }
        db.userInfo.insert_one(doc)
        user_info = db.userInfo.find_one({'id': kakao_id}, {"_id": False})

        payload = {
            'id': kakao_id,
            'name': kakao_nickname,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        ksign_up = True
        return token, user_info, ksign_up

    # 이미 회원이라면 토큰을 발급해서 로그인
    else:
        user_info = db.userInfo.find_one({'id': kakao_id}, {"_id": False})
        payload = {
            'id': kakao_id,
            'name': kakao_nickname,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        ksign_up = False
        return token, user_info, ksign_up


@application.route('/sign_up/save', methods=['POST'])
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
    payload = {
        'id': username_receive,
        'name': name_receive,
        'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jsonify({'result': 'success', 'token': token})


@application.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.userInfo.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@application.route('/sorted', methods=['GET'])
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
# 일부러 if문에서 널값 조회 후 널값일시 쓰레기값으로 반환
@application.route('/search', methods=['GET'])
def search():
    txt = request.args.get("txt")
    userdb = db.userInfo.find_one({'name': txt}, {'_id': False})
    if userdb is None:
        return
    else:
        return jsonify(userdb)


# 카운트
@application.route('/search/<txt>', methods=['PUT'])
def addcount(txt):
    db.userInfo.update_one({'name': txt}, {'$inc': {'countt': 1}})
    article = db.userInfo.find_one({'name': txt}, {'_id': False})
    return (article)


# countt 내림차순
@application.route('/order', methods=['GET'])
def order():
    orderlist = list(db.userInfo.find({}, {'_id': False}).sort([("countt", -1)]))
    return jsonify({"orderlist": orderlist})


# 리뷰 띄우기
@application.route('/reviews', methods=['GET'])
def review_listing():
    id = request.args.get("txt")
    reviews = list(db.tilreview.find({'owner':id}, {'_id': False}))
    return jsonify({'all_reviews':reviews})


@application.route('/reviews', methods=['POST'])
def review_post():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.userInfo.find_one({'id': payload['id']})

    id = request.form.get('id')
    reviewcontent = request.form.get('content')

    db.tilreview.insert({
        'owner': id,
        'writer': user_info['name'],
        'reviewcontent': reviewcontent
    })
    return {"result": "success"}


# 리뷰 삭제
@application.route('/delete', methods=['DELETE'])
def delete_review():
    content = request.args.get("txt")
    db.tilreview.delete_one({'reviewcontent': content})

    return jsonify({'msg': '삭제 완료!'})


# 카카오 로그인을 위한 인증 과정
@application.route('/oauth', methods=['GET'])
def oauthlogin():
    # code는 index.html에 카카오 버튼 url을 보면 알 수 있습니다. 버튼 url에 만든사람 인증id, return uri이 명시되어 있습니다.
    # 사용자 로그인에 성공하면 로그인 한 사람의 코드를 발급해줍니다.
    code = request.args.get("code")

    # 그 코드를 이용해 서버에 토큰을 요청해야 합니다. 아래는 POST 요청을 위한 header와 body입니다.
    client_id = KAKAO_CODE
    # redirect_uri = 'http://localhost:5000/oauth'
    redirect_uri = 'https://ohjinn.shop/oauth'
    token_url = "https://kauth.kakao.com/oauth/token"
    token_headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CODE,
        'redirect_uri': redirect_uri,
        'code': code
    }
    response = requests.post(url=token_url, headers=token_headers, data=data)
    token = response.json()
    # POST 요청에 성공하면 return value를 JSON 형식으로 파싱해서 담아줍니다.

    info_url = "https://kapi.kakao.com/v2/user/me"
    info_headers = {
        'Authorization': 'Bearer ' + token['access_token'],
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    info_response = requests.post(url=info_url, headers=info_headers)
    infos = info_response.json()
    if info_response.status_code == 200:
        token = kakao_sign_in(infos)
        if token[2] is False:
            response = make_response(redirect(url_for("index")))
            response.set_cookie(key='mytoken', value=token[0])
        else:
            response = make_response(redirect(url_for("my_page", id=token[1]['id'])))
            response.set_cookie(key='mytoken', value=token[0])
        return response
    else:
        return jsonify({'msg': '회원가입에 오류가 생겼습니다. 다시 시도해주세요'})


@application.route('/myPage/<id>')
def my_page(id):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.userInfo.find_one({"id": payload["id"]}, {"_id": False})
        status = (user_info != "")
        return render_template('myPage.html', user_info=user_info, status=status)
    except jwt.ExpiredSignatureError:
        return render_template('myPage.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('myPage.html', msg="로그인 정보가 존재하지 않습니다.")


@application.route('/update_profile', methods=['POST'])
def update_profile():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.userInfo.find_one({"id": payload["id"]}, {"_id": False})
        status = (user_info != "")

        password_receive = request.form['password_give']
        birth_receive = request.form['birth_give']
        url_receive = request.form['url_give']
        profile_receive = request.form['profile_give']
        password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

        new_doc = {
            "pw": password_hash,
            "birth": birth_receive,
            "url": url_receive,
            "profile_info": profile_receive
        }

        db.userInfo.update_one({'id': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


if __name__ == "__main__":
    application.debug = True
    application.run()

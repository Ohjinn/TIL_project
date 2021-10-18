import requests.exceptions
import urllib3.exceptions

import application
import boto3
import requests
import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


def getpic():
    users = list(application.db.userInfo.find({'url': {'$exists': True}}, {'_id': False}))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    print(users)
    for one in users:
        if 'https' in one['url']:
            try:
                name = one['name']
                url = one['url']
                data = application.requests.get(url)
                soup = application.BeautifulSoup(data.text, 'html.parser')
                imgurl = soup.select_one('meta[property="og:image"]')['content']

                extension = imgurl.split('.')[-1]
                if extension != 'png' and 'jpg' and 'jpeg':
                    extension = 'jpg'

                # urlretrieve는 다운로드 함수
                # application.urllib.request.urlretrieve(imgUrl, "static/images/" + name + '.jpg')
                tempimg = application.urllib.request.urlopen(imgurl).read()

                s3 = boto3.client('s3',
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                                  )
                s3.put_object(
                    ACL='public-read',
                    Bucket=BUCKET_NAME,
                    Body=tempimg,
                    Key='images/' + name + '.' + extension,
                    ContentType=tempimg.extention
                )

                application.db.userInfo.update_one({'name': name},
                                                   {'$set': {'pic': 'https://mysparta2.s3.ap-northeast-2.'
                                                                    'amazonaws.com/images/' + name + '.' + extension}})
            except urllib3.exceptions.LocationParseError:
                print('invalid url')
            except requests.exceptions.InvalidURL:
                print('invalid url')
        application.time.sleep(0.5)




def titlecrawling():
    users = list(application.db.userInfo.find({'url':{'$exists': True}}, {'_id': False}))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    print(users)

    newlist = []
    for x in users:
        tempname = x['name']
        tempurl = x['url']

        # 벨로그 크롤링
        if "velog.io" in tempurl:
            response = application.requests.get(tempurl)
            html = response.text
            soup = application.BeautifulSoup(html, 'html.parser')
            title = soup.select_one('div.sc-emmjRN')
            if title is None:
                title = soup.select_one('div.sc-ktHwxA')
            if title is None:
                title = soup.select_one('div.sc-krDsej')
            if title is None:
                title = soup.select_one('div.sc-gHboQg')
            if title is None:
                title = soup.select_one('div.sc-eilVRo')
            if title is None:
                title = soup.select_one('div.sc-jbKcbu')

            titles = title.select('a > h2')
            for title in titles:
                newlist.append({'name': tempname, 'title': title.text})

        # 티스토리 크롤링
        if "tistory.com" in tempurl:
            response = application.requests.get(tempurl)
            html = response.text
            soup = application.BeautifulSoup(html, 'html.parser')
            title = soup.select_one('ul.list_horizontal')
            if application.sys.getsizeof(title) < 100:
                title = soup.select('ul.list_category > li')
                for titles in title:
                    detail_title = titles.select_one('div.info > strong.name')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 100:
                title = soup.select('div.box-article > article')
                for titles in title:
                    detail_title = titles.select_one('a.link-article > strong')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 100:
                title = soup.select('div.article_skin > div.list_content')
                for titles in title:
                    detail_title = titles.select_one('a.link_post > strong')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 100:
                title = soup.select('div.inner > ul > li')
                for titles in title:
                    detail_title = titles.select_one('span.title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 100:
                title = soup.select('div.inner > div.post-item')
                for titles in title:
                    detail_title = titles.select_one('span.title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 100:
                title = soup.select('article.entry')
                for titles in title:
                    detail_title = titles.select_one('div.list-body')
                    detail_title = detail_title.select_one('h3')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 100:
                title = soup.select('div.area-common > article.article-type-common')
                for titles in title:
                    detail_title = titles.select_one('strong.title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 100:
                title = soup.select('div.wrap_content > div.content_list')
                for titles in title:
                    detail_title = titles.select_one('strong.txt_title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if application.sys.getsizeof(title) < 70:
                title = title.select('li')
                for titles in title:
                    detail_title = titles.select_one('div.box_contents > a')
                    newlist.append({'name': tempname, 'title': detail_title.text})


        # 크롤링 페이지를 켜기 위한 딜레이
        application.time.sleep(0.5)

    #최근에 저장한 타이틀 목록을 불러온다
    dbtitlelist = list(application.db.recentTitle.find({}, {'_id': False}))
    # dbuserstack = list(db.userStack.find({}, {'_id':False}))

    #만약 DB에 없는 제목 생긴 사람이 있으면 이름을 newstack에 저장
    newstack = []
    for x in newlist:
        tempname = x['name']
        temptitle = x['title']
        if x not in dbtitlelist:
            #임의의 제목 리스트가 DB리스트에 없으면 db리스트에 넣어주면서 최근에 변경이 감지된 사람을 스택에 저장한다.
            application.db.recentTitle.insert_one(x)
            if tempname not in newstack:
                print('now inserting name into stack')
                newstack.append(tempname)

    #userStack에서 최근 글이 쓰여진 사람을 목록에서 없애고 뒤에 붙임.
    for x in newstack:
        tempname = x
        application.db.userStack.delete_one({'name' : tempname})
        application.db.userStack.insert_one({'name' : tempname})
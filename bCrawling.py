import requests.exceptions
import urllib3.exceptions

import application
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

                application.urllib.request.urlretrieve(imgurl, "static/images/" + name + extension)
                application.db.userInfo.update_one({'name': name},
                                                   {'$set': {'pic': '../static/images/' + name + extension}})



                # tempimg = application.urllib.request.urlopen(imgurl).read()
                #
                # s3 = boto3.client('s3',
                #                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                #                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                #                   )
                # s3.put_object(
                #     ACL='public-read',
                #     Bucket=BUCKET_NAME,
                #     Body=tempimg,
                #     Key='images/' + name + '.' + extension,
                #     ContentType=tempimg.extention
                # )
                #
                # application.db.userInfo.update_one({'name': name},
                #                                    {'$set': {'pic': 'https://mysparta2.s3.ap-northeast-2.'
                #                                    'amazonaws.com/images/' + name + '.' + extension}})
                #


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

    newlist = []
    for x in users:
        tempname = x['name']
        tempurl = x['url']

        # ????????? ?????????
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

        # ???????????? ?????????
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


        # ????????? ???????????? ?????? ?????? ?????????
        application.time.sleep(0.5)

    #????????? ????????? ????????? ????????? ????????????
    dbtitlelist = list(application.db.recentTitle.find({}, {'_id': False}))
    # dbuserstack = list(db.userStack.find({}, {'_id':False}))

    #?????? DB??? ?????? ?????? ?????? ????????? ????????? ????????? newstack??? ??????
    newstack = []
    for x in newlist:
        tempname = x['name']
        temptitle = x['title']
        if x not in dbtitlelist:
            #????????? ?????? ???????????? DB???????????? ????????? db???????????? ??????????????? ????????? ????????? ????????? ????????? ????????? ????????????.
            application.db.recentTitle.insert_one(x)
            if tempname not in newstack:
                print('now inserting name into stack')
                newstack.append(tempname)

    #userStack?????? ?????? ?????? ????????? ????????? ???????????? ????????? ?????? ??????.
    for x in newstack:
        tempname = x
        application.db.userStack.delete_one({'name' : tempname})
        application.db.userStack.insert_one({'name' : tempname})
import app

def getPic():
    users = list(app.db.userInfo.find({}, {'_id': False}))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    for one in users:
        name = one['name']
        url = one['url']
        data = app.requests.get(url, headers=headers)
        soup = app.BeautifulSoup(data.text, 'html.parser')
        image = soup.select_one('meta[property="og:image"]')['content']

        imgUrl = image

        # urlretrieve는 다운로드 함수
        app.urllib.request.urlretrieve(imgUrl, "static/images/" + name + '.jpg')

        app.db.userInfo.update_one({'name': name}, {'$set': {'pic': '../static/images/' + name + '.jpg'}})

"""
웹 크롤링을 위한 컨트롤러. 일정시간마다 실행되게 하는 구현 필
"""
def titleCrawling():
    users = list(app.db.userInfo.find({}, {'_id': False}))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    newlist = []
    for x in users:
        tempname = x['name']
        tempurl = x['url']

        # 벨로그 크롤링
        if "velog" in tempurl:
            response = app.requests.get(tempurl)
            html = response.text
            soup = app.BeautifulSoup(html, 'html.parser')
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
        if "tistory" in tempurl:
            response = app.requests.get(tempurl)
            html = response.text
            soup = app.BeautifulSoup(html, 'html.parser')
            title = soup.select_one('ul.list_horizontal')
            if app.sys.getsizeof(title) < 100:
                title = soup.select('ul.list_category > li')
                for titles in title:
                    detail_title = titles.select_one('div.info > strong.name')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 100:
                title = soup.select('div.box-article > article')
                for titles in title:
                    detail_title = titles.select_one('a.link-article > strong')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 100:
                title = soup.select('div.article_skin > div.list_content')
                for titles in title:
                    detail_title = titles.select_one('a.link_post > strong')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 100:
                title = soup.select('div.inner > ul > li')
                for titles in title:
                    detail_title = titles.select_one('span.title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 100:
                title = soup.select('div.inner > div.post-item')
                for titles in title:
                    detail_title = titles.select_one('span.title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 100:
                title = soup.select('article.entry')
                for titles in title:
                    detail_title = titles.select_one('div.list-body')
                    detail_title = detail_title.select_one('h3')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 100:
                title = soup.select('div.area-common > article.article-type-common')
                for titles in title:
                    detail_title = titles.select_one('strong.title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 100:
                title = soup.select('div.wrap_content > div.content_list')
                for titles in title:
                    detail_title = titles.select_one('strong.txt_title')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            if app.sys.getsizeof(title) < 70:
                title = title.select('li')
                for titles in title:
                    detail_title = titles.select_one('div.box_contents > a')
                    newlist.append({'name': tempname, 'title': detail_title.text})


        # 크롤링 페이지를 켜기 위한 딜레이
        app.time.sleep(0.5)

    #최근에 저장한 타이틀 목록을 불러온다
    dbtitlelist = list(app.db.recentTitle.find({}, {'_id': False}))
    # dbuserstack = list(db.userStack.find({}, {'_id':False}))

    #만약 DB에 없는 제목 생긴 사람이 있으면 이름을 newstack에 저장
    newstack = []
    for x in newlist:
        tempname = x['name']
        temptitle = x['title']
        if x not in dbtitlelist:
            #임의의 제목 리스트가 DB리스트에 없으면 db리스트에 넣어주면서 최근에 변경이 감지된 사람을 스택에 저장한다.
            app.db.recentTitle.insert_one(x)
            if tempname not in newstack:
                print('now inserting name into stack')
                newstack.append(tempname)

    #userStack에서 최근 글이 쓰여진 사람을 목록에서 없애고 뒤에 붙임.
    for x in newstack:
        tempname = x
        app.db.userStack.delete_one({'name' : tempname})
        app.db.userStack.insert_one({'name' : tempname})
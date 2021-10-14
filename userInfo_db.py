from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbTil
db.userInfo.drop()

userInfo = [

    {"name": "이한솔", "url": "https://just-it.tistory.com/", "pic": ""},
    {"id": 123, "name": "권나연", "url": "https://velog.io/@hellonayeon", "pic": ""},
    {"name": "김다은", "url": "https://danykde0til.tistory.com/", "pic": ""},
    {"name": "양찬홍", "url": "https://l0u0l.tistory.com/", "pic": ""},
    {"name": "천소연", "url": "https://lu-delight.tistory.com/", "pic": ""},
    {"id": 234, "name": "김성훈", "url": "https://velog.io/@shkim1199", "pic": ""},
    {"name": "박형민", "url": "https://thalals.tistory.com/", "pic": ""},
    {"name": "서성혁", "url": "https://velog.io/@tjtjdgur0", "pic": ""},
    {"name": "김은아", "url": "https://bcoding-lab.tistory.com/", "pic": ""},
    {"name": "김수빈", "url": "https://soupnn.tistory.com/", "pic": ""},
    {"name": "이성우", "url": "https://lukaid.tistory.com/", "pic": ""},
    {"name": "신시우", "url": "https://velog.io/@siwoo", "pic": ""},
    {"name": "정태희", "url": "https://heendoong.tistory.com/", "pic": ""},
    {"name": "강현규", "url": "https://kkyu-coder.tistory.com/", "pic": ""},
    {"name": "장호진", "url": "https://ohjinn.tistory.com", "pic": ""},
    {"name": "송주현", "url": "https://thdwngus2.tistory.com/", "pic": ""},
    {"name": "유동민", "url": "https://cat-minzzi.tistory.com/", "pic": ""},
    {"name": "서태욱", "url": "https://velog.io/@apolontes", "pic": ""},
    {"name": "유제협", "url": "https://velog.io/@yu_jep", "pic": ""},
    {"name": "김경중", "url": "https://velog.io/@rudwnd33", "pic": ""},
    {"name": "김대현", "url": "https://velog.io/@dhk22", "pic": ""},
    {"name": "서지희", "url": "https://velog.io/@diheet", "pic": ""},
    {"name": "김지은", "url": "https://writerroom.tistory.com/category", "pic": ""},
    {"name": "김선만", "url": "https://velog.io/@manijang2", "pic": ""},
    {"name": "서재환", "url": "https://velog.io/@woodstock1993", "pic": ""},
    {"name": "윤영현", "url": "https://goodtoseeyou.tistory.com/", "pic": ""},
    {"name": "김우진", "url": "https://velog.io/@dnwlsrla40", "pic": ""},
    {"name": "신한국", "url": "https://codari.tistory.com/", "pic": ""},
    {"name": "김혜린", "url": "https://khr5830.tistory.com/", "pic": ""},

]

db.userInfo.insert_many(userInfo)

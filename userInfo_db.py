from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbTil
db.userInfo.drop()
userInfo = [
    {
        "name": "김성훈",
        "id": 1955598890,
        "pw": "30cd4a85fc09f6959b4c7807b4120c3e55e08204cc82c913e3cc7687b500eec2",
        "url": "https://velog.io/@shkim1199",
        "birth": "1999-07-26",
        "profile_info": "젊었을 때 배움을 게을리 한 사람은 과거를 상실하며 미래도 없다",
        "countt": 7,
        "pic": ""
    },
    {
        "id": "hjin9445",
        "pw": "3bf8ee65b7b961278e7d216bb1be7d2659cebdbd66907649247f20aaef085c27",
        "name": "장호진",
        "birth": "2021-12-31",
        "url": "https://ohjinn.tistory.com/",
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": "",
        "pic": "https://mysparta2.s3.ap-northeast-2.amazonaws.com/images/장호진.png",
        "countt": 4
    },
    {
        "id": "tjwlgml",
        "pw": "ecebedc0eb0987fcf5ffdac2529c1508a54d758f91b4b7ee6168ba5c91a152ec",
        "name": "서지희",
        "birth": "2021-12-31",
        "url": "https://velog.io/@diheet",
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": "안녕하세요~!",
        "countt": 9,
        "pic": "https://mysparta2.s3.ap-northeast-2.amazonaws.com/images/서지희.png"
    },
    {
        "id": "dbsdudgus",
        "pw": "ecebedc0eb0987fcf5ffdac2529c1508a54d758f91b4b7ee6168ba5c91a152ec",
        "name": "윤영현",
        "birth": "2021-10-20",
        "url": "https://goodtoseeyou.tistory.com/",
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": "",
        "pic": "https://mysparta2.s3.ap-northeast-2.amazonaws.com/images/윤영현.png",
        "countt": 2},
    {
        "id": 1955597733,
        "pw": "30cd4a85fc09f6959b4c7807b4120c3e55e08204cc82c913e3cc7687b500eec2",
        "name": "현규",
        "countt": 1
    },
    {
        "id": 1947914319,
        "pw": "30cd4a85fc09f6959b4c7807b4120c3e55e08204cc82c913e3cc7687b500eec2",
        "name": "장호진",
        "birth": "",
        "profile_info": "안녕",
        "url": "https://ohjinn.tistory.com/"
    },
    {
        "id": "chanhong",
        "pw": "3bf8ee65b7b961278e7d216bb1be7d2659cebdbd66907649247f20aaef085c27",
        "name": "양찬홍",
        "birth": "2021-12-31",
        "url": "https://l0u0l.tistory.com/",
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": "",
        "pic": "..static/images/양찬홍.png",
        "countt": 1
    },
    {
        "id": "chanho",
        "pw": "3bf8ee65b7b961278e7d216bb1be7d2659cebdbd66907649247f20aaef085c27",
        "name": "이찬호",
        "birth": "2021-12-31",
        "url": "https://anndeveloper.tistory.com//",
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": "",
        "pic": "..static/images/이찬호.png",
        "countt": 1
    }
]
db.userInfo.insert_many(userInfo)

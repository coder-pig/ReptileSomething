# 抓取Gank.io所有文章的爬虫

import pymysql
import requests as rq
import urllib
import coderpig_n as cn

gank_api = "http://gank.io/api/data/"

# 各种分类的表名：Android，iOS，休息视频，福利，拓展资源，前端，瞎推荐，App
category_list = ["android", "ios", "video", "meizi", "other", "fed", "random", "app"]
type_list = ["Android", "iOS", "休息视频", "福利", "拓展资源", "前端", "瞎推荐", "App"]
column_list = ('_id', 'dsec', 'images', 'url', 'type')


def init_db():
    db = pymysql.connect(host='localhost', user='root', password='zpj12345', port=3306, db='gank', charset="utf8")
    cursor = db.cursor()
    try:
        for category in category_list:
            sql = "CREATE TABLE IF NOT EXISTS %s (" \
                  "_id  VARCHAR(50) NOT NULL," \
                  "dsec VARCHAR(500) DEFAULT ''," \
                  "images  VARCHAR(500) DEFAULT ''," \
                  "url  TEXT," \
                  "type VARCHAR(50)  DEFAULT ''," \
                  "PRIMARY KEY (_id))" % category
            cursor.execute(sql)
        db.close()
    except:
        pass


class Gank:
    _id = dsec = images = url = type = ''

    def __init__(self, _id, dsec, images, url, type):
        self._id = _id
        self.dsec = dsec
        self.images = images
        self.url = url
        self.type = type

    # 打印对象内容
    def to_value_tuple(self):
        return self._id, self.dsec, self.images, self.url, self.type


def insert_db(gank_list):
    db = pymysql.connect(host='localhost', user='root', password='zpj12345', port=3306, db='gank', charset="utf8")
    cursor = db.cursor()
    try:
        for data in gank_list:
            if data.type in type_list:
                category = category_list[type_list.index(data.type)]
                data_tuple = data.to_value_tuple()
                sql = "INSERT INTO {table}({keys}) VALUES ({values})".format(table=category,
                                                                             keys=','.join(column_list),
                                                                             values=','.join(['%s'] * len(data_tuple)))
                print(sql)
                cursor.execute(sql, data_tuple)
        db.commit()
    except Exception as e:
        print(str(e))
        db.rollback()
    db.close()


def spider_data(pos):
    count = 1
    while True:
        resp = rq.get(gank_api + urllib.parse.quote(type_list[pos]) + "/50/" + str(count), proxies=cn.get_proxy_ip())
        resp_json = resp.json()
        print(resp.url)
        if resp.status_code == 200 and len(resp_json['results']) != 0:
            json_list = []
            for result in resp_json['results']:
                gank = Gank(result['_id'], result['desc'], result.get('images', ''), result.get('url', ''),
                            result['type'])
                json_list.append(gank)
            insert_db(json_list)
        else:
            break
        count += 1


if __name__ == '__main__':
    # db = pymysql.connect(host='localhost', user='root', password='zpj12345', port=3306, charset="utf8")
    # cursor = db.cursor()
    # cursor.execute("CREATE DATABASE gank DEFAULT CHARACTER SET utf8")
    # db.close()
    init_db()
    for i in range(0, len(type_list)):
        spider_data(i)

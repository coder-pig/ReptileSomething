# 拉勾网Android招聘数据分析
import urllib.parse
import requests
import xlwt
import xlrd
import tools as t

# Ajax加载url
ajax_url = "https://www.lagou.com/jobs/positionAjax.json?"

# url拼接参数
request_params = {'px': 'default', 'city': '深圳', 'needAddtionalResult': 'false', 'isSchoolJob': '0'}

# post提交参数
form_data = {'first': 'false', 'pn': '50', 'kd': 'android'}

# 模拟请求头
ajax_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 '
                  'Safari/537.36',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.lagou.com/jobs/list_android?labelWords=&fromSearch=true&suginput='
}


# 获取每页招聘信息
def fetch_data(page):
    fetch_url = ajax_url + urllib.parse.urlencode(request_params)
    try:
        resp = requests.post(url=fetch_url, data=form_data, headers=ajax_headers)
        if resp.status_code == 200:
            print(resp.text)
            return
    except Exception as e:
        print(e)

# 处理数据

if __name__ == '__main__':
    fetch_data(0)

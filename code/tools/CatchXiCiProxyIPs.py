import coderpig_n as cpn
import requests

# 抓取速度较快的西刺代理ip

headers = {
    'User-Agent': cpn.user_agent_dict['chrome'],
    'Host': 'www.xicidaili.com'
}

base_url = 'http://www.xicidaili.com/nn/'


def catch_page_count():
    while True:
        proxy_ip = {'http': 'http://' + cpn.get_dx_proxy_ip()}
        try:
            resp = requests.get(base_url, headers=headers, proxies=proxy_ip, timeout=5)
            if resp is not None:
                print(proxy_ip)
                soup = cpn.get_bs(resp.text)
                # 获得最后一页页码
                last_page_count = soup.find('div', attrs={'class', 'pagination'}).findAll('a')[-2].get_text()
                return last_page_count
        except Exception as e:
            pass


def catch_ip(url):
    while True:
        proxy_ip = {'http': 'http://' + cpn.get_dx_proxy_ip()}
        print(proxy_ip)
        try:
            resp = requests.get(url, headers=headers, proxies=proxy_ip,timeout=10)
            if resp is not None:
                soup = cpn.get_bs(resp.text)
                trs = soup.find('table').findAll('tr')[1:]
                for tr in trs:
                    if float(tr.find('div', attrs={'bar'})['title'][:-1]) > 1:
                        tds = tr.findAll('td')
                        cpn.write_xc_ip_file(tds[1].get_text() + ":" + tds[2].get_text())
        except Exception as e:
            pass


if __name__ == '__main__':
    page_count = catch_page_count()
    print(page_count)
    if page_count is not None:
        for i in range(1, int(page_count) + 1):
            print("========== 开始抓取第%d页 ==========" % i)
            page_url = base_url + str(i)
            catch_ip(page_url)
            print("========== 第%d页抓取完毕 ==========" % i)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle

login_url = 'https://passport.csdn.net/account/login'
csdn_url = 'https://www.csdn.net/'


# 自动登陆后保存Cookie
def auto_login():
    browser = webdriver.Chrome()
    browser.delete_all_cookies()
    browser.get(login_url)
    browser.find_element_by_id("username").send_keys(u"xxx@qq.com")
    browser.find_element_by_id("password").send_keys(u"xxx")
    login_btn = browser.find_element_by_class_name('logging').click()
    # 获得当前的url，可以利用这个和登陆链接做对比，不同则说明登陆成功
    print(browser.current_url)
    # 利用pickle序列化保存下来
    pickle.dump(browser.get_cookies(), open('cookies.pkl', 'wb'))
    browser.quit()


# 使用Cookie访问，验证右上角是否有登陆用户名即可只是是否登陆成功
def cookie_browse():
    browser = webdriver.Chrome()
    browser.get(csdn_url)
    browser.delete_all_cookies()
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print(cookies[0])
    print(type(cookies[0]))
    for cookie in cookies:
        browser.add_cookie({
            "domain": ".csdn.net",  # 火狐浏览器不用填写，谷歌要需要
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expiry": cookie.get('expiry'),
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        })
    browser.get(csdn_url)
    time.sleep(20)


cookie_browse()

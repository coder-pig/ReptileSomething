from appium import webdriver
import time

search_name = "阿里"


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '5.1',
    'deviceName': 'TA0900409U',
    'unicodeKeyboard': 'True',
    'resetKeyboard': 'True',
    'appPackage': 'com.tencent.mm',
    'appActivity': 'com.tencent.mm.ui.LauncherUI',
    'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(1)
driver.find_element('xpath', "//android.widget.Button[@text='登录']").click()
time.sleep(1)
driver.find_element('xpath', "//android.widget.EditText[@text='请填写手机号']").send_keys('')
time.sleep(2)
driver.find_element('xpath', "//android.widget.Button[@text='下一步']").click()
time.sleep(2)
driver.find_element('xpath', "//android.widget.EditText[@text='']").send_keys('')
driver.find_element('xpath', "//android.widget.Button[@text='登录']").click()
time.sleep(5)
driver.find_element('xpath', "//android.widget.Button[@text='否']").click()
time.sleep(20)
driver.find_element('xpath', "//android.widget.TextView[@text='通讯录']/../..").click()
time.sleep(1)
driver.find_element('xpath', "//android.widget.TextView[@text='公众号']/../../..").click()
driver.find_element('xpath', "//android.widget.ImageButton[@content-desc='搜索']").click()
driver.find_element('xpath', "//android.widget.EditText[@text='搜索']").send_keys(search_name)
time.sleep(2)
el = driver.find_element('class name', 'android.widget.ListView')
item_list = el.find_elements('class name', 'android.widget.LinearLayout')
if len(item_list) > 0:
    item_list[0].click()
driver.find_element('xpath', "//android.widget.ImageButton[@content-desc='聊天信息']").click()
driver.find_element('xpath', "//android.widget.TextView[@text='查看历史消息']/../..").click()
time.sleep(5)
print(driver.page_source)
view_list = driver.find_elements('xpath', '//android.webkit.WebView//android.webkit.WebView/android.view.View')
# driver.find_element('xpath',"//android.view.View[@content-desc='聊天信息']")
view_list[4].click()

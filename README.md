# ReptileSomething

标签: 测试

## 用Python抓点东西玩玩

## **我的简易模块：coderpig.py**

- init_https()：启用Https支持
- get_resp(url, headers=None, proxy=None, read=True)：根据url获得resp
- download_pic(url, dir_name, proxy=None, headers=None)：图片下载
- load_data(file_path)：按行读取文件里的内容添加到列表中返回
- write_list_data(content_list, file_path, type="w+")：把列表里的内容按行写入到文件中
- write_str_data(content, file_path, type="a+")：往文件追加字符串
- get_bs(html, online=True)：获得一个BeautifulSoup对象(默认在线，可以加载本地html)
- init_browser()：初始化一个无界面浏览器
- is_dir_existed(path, mkdir=True)：判断路径是否存在，不存在默认新建
- get_proxy_ip()：随缘取出一枚代理ip


## 1.抓取图片

- **GankPicCatch.py**：抓取gank.io所有的妹子图
- **FuliShePicCatch.py**：抓取 http://www.zhangzishi.cc/ 中的福利社专题妹子图
- **win400MeituCatch.py**：抓取 http://www.win4000.com/meitu.html 上所有妹子图
- **CatchAiTaoTuPic.py**：抓取 https://www.aitaotu.com/taotu/ 爱套图里的美女图
- **CatchTuChongPic.py**：抓取 https://tuchong.com/tags/%E7%A7%81%E6%88%BF 图虫的私房妹子图
- **CatchJianDanMeiziPic.py**：抓取 http://jandan.net/ooxx 煎蛋网妹子图
- **CatchMWeiboPic.py**：抓取 新浪微博某博主的图片，可自行替换id以及爬取页数
- **CatchHuaBanPic.py**：抓取花瓣网某个用户所有的画板里的图片
- **CatchBcyCosPic.py**：抓取半次元所有的每日热门Coser图片
- **CatchTieBaPic.py**:抓取百度贴吧某个帖子里所有的图片(多页)

## 2.抓取数据

- **CatchCityCode.py**：抓取所有的城市编码(天气查询用到)
- **CatchPostCode.py**：抓取所有的邮政编码与电话区号
- **CatchIdCardAreaCode.py**：抓取所有身份证前六位对应的行政区划代码(貌似失效了)
- **CatchIdCardAreaCodeN.py**：抓取所有身份证前六位对应的行政区划代码
- **CsdnLogin.py**：CSDN模拟登录保存Cookie并使用Cookie访问
- **CatchWeChatRes.py**：抓取微信公众号文章里的所有图片，音频和视频

## 3.工具脚本

- **CsdnReaderHelper.py**：刷CSDN博客访问量

## 生成文件：

- city_code.txt：城市编码，天气查询用
- id_card_area_code.txt：身份证前六位对应行政区代码
- post_code.txt：邮政编码与电话区号
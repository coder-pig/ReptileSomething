# ReptileSomething



## 项目简介

用Python弄点有趣的东西玩玩，抓抓小姐姐，写写工具脚本，
抓点有用数据，做下数据分析，后面会学学写后台～

![][1]

## 项目结构

一开始因为没有统一输入输出限定，项目结构，项目乱糟糟的，
2018.3.22 花了一下午整理了一下结构：

```
├── build (执行相关目录)
│   └── outputs (生成文件目录)
│       ├── documents (生成文档目录)
│       ├── logs (生成日志目录，中途过渡用)
│       ├── pictures (生成图片目录)
│       └── videos (生成非图片类资源目录)
├── code (代码存放目录)
│   ├── analysis (数据分析类)
│   │   ├── CatchWorkingReport.py (抓取2018年政府报告高频词做词云)
│   │   └── LGDataAnalysis.py (拉取拉勾网2018年Android岗位相关做数据分析)
│   ├── meizi (图片抓取类)
│   │   ├── CatchAiTaoTuPic.py (抓取爱套图网妹子图)
│   │   ├── CatchBcyCosPic.py (抓取半次元Cos图)
│   │   ├── CatchHuaBanPic.py (抓取花瓣网妹子图)
│   │   ├── CatchJianDanMeiziPic.py (抓取煎蛋网妹子图)
│   │   ├── CatchMWeiboPic.py (抓取某个微博里的所有图)
│   │   ├── CatchTieBaPic.py (抓取某个贴吧链接里的所有图片)
│   │   ├── CatchTuChongPic.py (抓取图虫妹子图)
│   │   ├── FuliShePicCatch.py (抓取福利社妹子图)
│   │   ├── GankPicCatch.py (抓取GankIO妹子图)
│   │   └── win400MeituCatch.py (抓取win400妹子图)
│   └── tools (工具类)
│       ├── CatchCityCode.py (抓取城市编码)
│       ├── CatchDoubanMusic250.py (抓取豆瓣音乐250写入Excel)
│       ├── CatchIdCardAreaCodeN.py (抓取身份证前6位地区码，新)
│       ├── CatchIdCardAreaCode.py (抓取身份证前6位地区码，旧)
│       ├── CatchPostCode.py (抓取邮政编码)
│       ├── CatchWeChatRes.py (抓取某篇微信文章里所有的图片，语音，视频)
│       ├── CatchXiCiProxyIPs.py (抓取西刺代理中速度较快的代理ip)
│       ├── CsdnLogin.py (CSDN模拟登录)
│       └── CsdnReaderHelper.py (刷CSDN博客访问量脚本)
├── coderpig_n.py (自己写简易工具模块，版本2)
├── coderpig.py (自己写简易工具模块，版本1)
├── config.py (配置文件，目前主要用于指定输出路径)
├── LICENSE (授权文件)
├── proxy_ip.txt (代理ip列表文件)
├── README.md
├── res (代码运行所需的资源，比如字体，图片等等)
│   ├── documents
│   └── pictures
└── tools.py (自己写简易工具模块，版本3)

```

## 项目说明

不定期更新脚本，脚本失效了，或者你有想抓的网站，想做的小工具，
欢迎提issues，可以加下我微信，拉你进群一起学习Py！

![][2]

我写过的Python教程可见：[https://juejin.im/user/570afb741ea493005de84da3][3]





  [1]: http://static.zybuluo.com/coder-pig/y0qln52j7cg4f39wzf2muh8m/1.gif
  [2]: http://static.zybuluo.com/coder-pig/qaadbz1aml70m4jaw7712p9x/1.png
  [3]: https://juejin.im/user/570afb741ea493005de84da3
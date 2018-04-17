import pandas as pd
import numpy as np

# s1 = pd.Series([1, 2, 3, np.nan, 5])
# print("1.通过列表创建Series对象：\n%s" % s1)
# s2 = pd.Series([1, 2, 3, np.nan, 5], index=['a', 'b', 'c', 'd', 'e'])
# print("2.通过列表创建Series对象(自定义索引)：\n%s" % s2)
# print("3.通过索引获取元素：%s" % s2['a'])
# print("4.获得索引：%s" % s2.index)
# print("5.获得值：%s" % s2.values)
# print("6.和列表一样值支持分片的：\n{}".format(s2[0:2]))
# s3 = pd.Series(pd.date_range('2018.3.17', periods=6))
# print("7.利用date_range生成日期列表:\n%s" % s3)

# 1.创建DataFrame对象
dict1 = {
    '学生': ["小红", "小绿", "小蓝", "小黄", "小黑", "小灰"],
    '性别': ["女", "男", "女", "男", "男", "女"],
    '年龄': np.random.randint(low=10, high=15, size=6),
}
d1 = pd.DataFrame(dict1)
print("1.用相等长度的列表组成的字典对象生成：\n %s" % d1)

d2 = pd.DataFrame(np.random.randint(low=60, high=100, size=(6, 3)),
                  index=["小红", "小绿", "小蓝", "小黄", "小黑", "小灰"],
                  columns=["语文", "数学", "英语"])
print("2.通过二维数组生成DataFrame: \n %s" % d2)

# 2.数据查看
print("3.head函数查看顶部多行(默认5行)：\n%s" % d2.head(3))
print("4.tail函数查看底部多行(默认5行)：\n%s" % d2.tail(2))
print("5.index查看所有索引：%s" % d2.index)
print("6.columns查看所有行标签：%s" % d2.columns)
print("7.values查看所有值:\n%s" % d2.values)

# 3.数据排序
print("8.按索引排序(axis=0行索引，=1列索引排序，ascending=False降序排列):\n%s"
      % (d2.sort_index(axis=0, ascending=False)))
print("9.按值进行排序：\n%s" % d2.sort_values(by="语文", ascending=False))

# 4.数据选择
print("9.选择一列或多列:\n{} {} ".format(d2['语文'], d2[['数学', '英语']]))
print("10.数据切片:\n{}".format(d2[0:1]))
print("11.条件过滤(过滤语文分数高于90的数据):\n{}".format(d2[d2.语文 > 90]))
print("12.loc函数行索引切片获得指定列数据：\n{}".format(d2.loc['小红':'小蓝', ['数学', '英语']]))
print("13.iloc函数行号切片获得指定列数据：\n{}".format(d2.iloc[4:6, 1:2]))

# 5.求和，最大/小值，平均值，分组
print("14.语文总分：{}".format(d2['语文'].sum()))
print("15.语文平均分：{}".format(d2['语文'].mean()))
print("16.数学最高分：{}".format(d2['数学'].max()))
print("17.英语最低分：{}".format(d2['英语'].min()))

# 6.数据输入输出(可以把数据保存到csv或excel中，也可以读取文件)
d1.to_csv('student_1.csv')
d3 = pd.read_csv('student_1.csv')
print("读取csv文件中的数据：\n{}".format(d3))
d2.to_excel('student_2.xlsx', sheet_name="Sheet1")
d4 = pd.read_excel('student_2.xlsx', sheet_name="Sheet1")
print(("读取excel文件中的数据：\n{}".format(d4)))

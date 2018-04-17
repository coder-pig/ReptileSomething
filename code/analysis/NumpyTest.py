import numpy as np

# 1.访问数组
a1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("访问第一行: %s" % a1[0])
a1[0] = 2  # 修改数组中元素的值
print("访问第一列: %s" % a1[:, 0])
print("访问前两行:\n {}".format(a1[:2]))
print("访问前两列:\n {}".format(a1[:, :2]))
print("访问第二行第三列：{}".format(a1[1][2]))

# 2.通过take函数访问数组(axis参数代表轴)，put函数快速修改元素值
a2 = np.array([1, 2, 3, 4, 5])
print("take函数访问第二个元素：%s" % a2.take(1))
a3 = np.array([0, 2, 4])
print("take函数参数列表索引元素：%s" % a2.take(a3))
print("take函数访问某个轴的元素：%s" % a1.take(1, axis=1))
a4 = np.array([6, 8, 9])
a2.put([0, 2, 4], a4)
print("put函数快速修改特定索引元素的值：%s" % a2)

# 3.通过比较符访问元素
print("通过比较符索引满足条件的元素：%s" % a1[a1 > 3])

# 4.遍历数组
print("一维数组遍历：")
for i in a2:
    print(i, end=" ")
print("\n二维数组遍历：")
for i in a1:
    print(i, end=" ")
print("\n还可以这样遍历：")
for (i, j, k) in a1:
    print("%s - %s - %s" % (i, j, k))

# 5.insert插入元素(参数依次为：数组，插入轴的标号，插入值，axis=0插入行，=1插入列)
a5 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
a5 = np.insert(a5, 0, [6, 6, 6], axis=0)
print("insert函数插入元素到第一行：\n %s " % a5)

# 6.delete删除元素(参数依次为数组，删除轴的标号，axis同上)
a5 = np.delete(a5, 0, axis=1)
print("delete函数删除第一列元素：\n %s" % a5)

# 7.copy深拷贝一个数组,直接赋值是浅拷贝
a6 = a5.copy()
a7 = a5
print("copy后的数组是否与原数组指向同一对象：%s" % (a6 is a5))
print("赋值的数组是否与原数组指向同一对象：%s" % (a7 is a5))

# 8.二维数组转一维数组，二维数组数组合并
a8 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("二维数组 => 一维数组：%s" % a8.flatten())
a9 = np.array([[1, 2, 3], [4, 5, 6]])
a10 = np.array([[7, 8], [9, 10]])
print("两个二维数组合并 => 一个二维数组：\n{}".format(np.concatenate((a9, a10), axis=1)))

# 9.数学计算(乘法是对应元素想成，叉乘用.dot()函数)
a11 = np.array([[1, 2], [3, 4]])
a12 = np.array([[5, 6], [7, 8]])
print("数组相加：\n%s" % (a11 + a12))
print("数组相减：\n%s" % (a11 - a12))
print("数组相乘：\n%s" % (a11 * a12))
print("数组相除：\n%s" % (a11 / a12))
print("数组叉乘:\n%s" % (a11.dot(a12)))

# 10.其他
a12 = np.array([1, 2, 3, 4])
print("newaxis增加维度：\n %s" % a12[:, np.newaxis])
print("tile函数重复数组(重复列数，重复次数)：\n %s" % np.tile(a12, [2, 2]))
print("vstack函数按列堆叠：\n %s" % np.vstack([a12, a12]))
print("hstack函数按行堆叠：\n %s" % np.hstack([a12, a12]))
a13 = np.array([1, 4, 8, 2, 44, 77, -2, 1, 4])
a13.sort()
print("sort函数排序：\n %s" % a13)
print("unique函数去重：\n {}".format(np.unique(a13)))

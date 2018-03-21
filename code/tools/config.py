import os
import sys

"""
    相关配置
    1.对应的文件输出路径
"""
build_path = os.path.split(os.path.realpath(__file__))[0]
print(build_path)
print(sys.path[0])
print(sys.argv[0])
print(os.getcwd())

import os

"""
    相关配置
    1.对应的文件输出路径
"""
# 工程目录
root_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))

# 生成文件目录
build_path = os.path.join(root_path, 'build')
outputs_path = os.path.join(build_path, 'outputs')
outputs_documents_path = os.path.join(outputs_path, "documents")
outputs_logs_path = os.path.join(outputs_path, "logs")
outputs_pictures_path = os.path.join(outputs_path, "pictures")
outputs_video_path = os.path.join(outputs_path, "videos")

# res 资源目录
res_path = os.path.join(root_path, "res")
res_documents = os.path.join(res_path, "documents")
res_pictures = os.path.join(res_path, "pictures")

# 代码目录
code_path = os.path.join(root_path + "code")
code_meizi_path = os.path.join(code_path , "meizi")
code_tools_path = os.path.join(code_path , "tools")
code_analysis_path = os.path.join(code_path , "analysis")
code_threading_path = os.path.join(code_path , "threading")

if __name__ == '__main__':
    print(root_path)
    print(build_path)
    print(outputs_path)
    print(outputs_documents_path)
    print(outputs_logs_path)
    print(outputs_pictures_path)
    print(outputs_video_path)
    print(res_path)
    print(res_documents)
    print(res_pictures)

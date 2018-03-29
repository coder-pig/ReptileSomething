import os


"""
    相关配置
    1.对应的文件输出路径
"""
# 工程目录
root_path = os.path.abspath(os.path.join(os.getcwd(), "../../"))

# 生成文件目录
build_path = root_path + "/build/"
outputs_path = build_path + "outputs/"
outputs_documents_path = outputs_path + "documents/"
outputs_logs_path = outputs_path + "logs/"
outputs_pictures_path = outputs_path + "pictures/"
outputs_video_path = outputs_path + "videos/"

# res 资源目录
res_path = root_path + "/res/"
res_documents = res_path + "documents/"
res_pictures = res_path + "pictures/"

# 代码目录
code_path = root_path + "/code/"
code_meizi_path = code_path + "meizi/"
code_tools_path = code_path + "tools/"
code_analysis_path = code_path + "analysis/"
code_threading_path = code_path + "threading/"

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


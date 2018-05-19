from flask import Flask, request, url_for, render_template

app = Flask(__name__)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        datas = request.items()
        for data in datas:
            print(data.get('user',''))
            print(data.get('password',''))
        return ''
    if request.method == 'POST':
        # 遍历参数
        return render_template('login.html', name=request.form.get('name', ''),
                               password=request.form.get('password', ''))


if __name__ == '__main__':
    app.run(debug=True)

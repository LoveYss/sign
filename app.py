from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_cors import CORS
import base64
import os, time, json
import know_face
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/sign_user"
# app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class SignUser(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    user_img = db.Column(db.String(1000), unique=True)
    sign_date = db.Column(db.String(100), default='')

    def __repr__(self):
        return '%s' % self.name


# 解决跨域
CORS(app, supports_credentials=True)

# db.create_all()
# img_path = os.path.dirname(__file__) + '\\static\\images\\user_img.jpg'
# user1 = SignUser(name='wjl', user_img=img_path)
# db.session.add(user1)
# db.session.commit()


@app.route('/index', methods=['POST', 'GET'])
def index():
    user_img_data = SignUser.query.get(1)
    today = time.strftime('%d', time.localtime(time.time()))
    history = str(user_img_data.sign_date)[1:].split(',')
    if today in history:
        return redirect(url_for('date'))
    img_data = request.args.get('users_img')
    if img_data:
        # print(img_data[22:])
        img = base64.b64decode(img_data[22:])
        # 将base64转为图片；img_data[22:]才是base64的编码
        file = open('static/images/unknown_users_img.jpg', 'wb')
        file.write(img)
        file.close()
    return render_template('index.html')


@app.route('/sign', methods=['POST', 'GET'])
def requests():
    user_img_data = SignUser.query.get(1)
    history = str(user_img_data.sign_date)[1:].split(',')
    int_his = []
    [int_his.append(int(i)) for i in history]
    return jsonify({'cal': int_his})


@app.route('/sign_date')
def date():
    user_img_data = SignUser.query.get(1)
    today = time.strftime('%d', time.localtime(time.time()))
    history = str(user_img_data.sign_date)[1:].split(',')
    detection = know_face.validation(user_img_data.user_img)
    if detection:
        if today not in history:
            history.append(today)
            user_img_data.sign_date = ''.join(history) + ','
            db.session.commit()
        return render_template('request.html')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

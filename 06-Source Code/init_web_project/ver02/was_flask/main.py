import re
from flask import Flask, jsonify, request, render_template, make_response, session, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from werkzeug.utils import secure_filename
from server_view import view
from server_controller.user_setting import User
import os
import random

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
# CORS(app)
# app.secret_key = '1trillionKey'
mtplNum=10**15
app.secret_key = str(int(random.random()*mtplNum))
# print(app.secret_key)

app.register_blueprint(view.main_obj, url_prefix='/service')
app.register_blueprint(view.acc_obj, url_prefix='/account')
login_manager = LoginManager()
login_manager.init_app(app)
# session을 보다 복잡하게 만들어준다.
login_manager.session_protection = 'strong'

app.config['UPLOAD_FOLDER'] = './'


# 테스트 검증 완료
@app.route('/') # 접속할 URL
def home():
    return redirect('/service/signin')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

# @app.before_request
# def app_before_request():
#     if 'client_id' not in session:
#         session['client_id'] = request.environ.get(
#             'HTTP_X_REAL_IP', request.remote_addr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

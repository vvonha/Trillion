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
login_manager = LoginManager()
login_manager.init_app(app)
# session을 보다 복잡하게 만들어준다.
login_manager.session_protection = 'strong'

app.config['UPLOAD_FOLDER'] = './'



# 테스트 검증 완료
@app.route('/') # 접속할 URL
def home():
    return redirect('/service/signin')

# 테스트 검증 완료
@app.route('/register_1', methods=['GET','POST']) # 접속할 URL
def register_level_1():
	return render_template('register_1.html')

@app.route('/register_2', methods=['GET','POST']) # 접속할 URL
def register_level_2():
    return render_template('register_2.html', sort=3, username='-')

# [ id 검증 함수 ]
@app.route('/examine_id_value', methods=['GET','POST']) # 접속할 URL
def examine_id_value():
    username=request.form['username']
    print('\n\nTTTTTTEST:',username,'\n\n')
    user=User.find(username)
    print(user)
    if(user == None):
        return render_template('register_2.html', sort=1, username=username)
    else:
        return render_template('register_2.html', sort=2, username='-')

@app.route('/register_3', methods=['GET','POST']) # 접속할 URL
def register_level_3():
    print('level = 3')
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    
    # 33-47
    # 58-64
    # 91-96
    # for(pass)
    return render_template('register_3.html', username=username, password=password)

def examine(text, str, start_idx, end_str):
        print(str)
        if text.find(str,start_idx) != -1:
            i=text.find(str)
            # examine
            examine=text[i+len(str):text.find(end_str,i)]
            examined = re.sub(r"[^a-zA-Z0-9,]","", examine)
            # exam.replace('[',''); exam.replace(']',''); exam.replace('|',''), exam.replace('l','')
            # exam.replace('I',''); exam.replace('L',''); exam.replace('!','')
            print(examined); print()
            return(examined)
            # print(text[i+len("Patient's Name: "):text.find(' ',i)])
            
@app.route('/register_3_temp', methods=['GET','POST']) # 접속할 URL
def register_level_3_temp():
    print('level = 3_temp')
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    
    
    # Test Code
    file = request.files['file']
    file_and_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_and_path)
    #return 'file uploaded successfully'
    
    opened_file = open(file_and_path, 'r', encoding='UTF8')
    text=''.join(opened_file.readlines())
    # text=opened_file.readlines()
    # print(text)
    
    if "Patient's Name:" in text:
        print('Exist!')
        
    # start=80
    # while("Patient's Name:" in text):
    #     i=text.find('P',start) # 100
    #     if i==-1:
    #         break
    #     start=i+1
    #     print('i:',i)
    #     print(text[i:i+16])
    #     # if text[i:i+15]=="Patient's Name: ":
    #     #     print(text[i+16:i+30])
    
    Patient=examine(text, "Patient's Name:", 100, "Date of birth:")
    birth=examine(text, "Date of birth:", 100, "Ward:")
    Ward=examine(text, "Ward:", 100, "Hospital:")
    Hospital=examine(text, "Hospital:", 100, "Consultant:")
    Consultant=examine(text, "Consultant:", 100, "\n")
    
    
    # result(검증 문자열) 추가된 것 확인
    return render_template('register_3_temp.html', username=username, password=password, 
                           Patient=Patient, birth=birth, Ward=Ward, Hospital=Hospital, Consultant=Consultant)

@app.route('/register_4', methods=['GET','POST']) # 접속할 URL
def register_level_4():
    print('level = 4')
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    
    User.create(request.form['username'], request.form['password'])
    return render_template('register_4.html', username=username, password=password)

@app.route('/complete', methods=['GET','POST']) # 접속할 URL
def register_complete():
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    return render_template('signin.html', username=username, password=password, flag=True)

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

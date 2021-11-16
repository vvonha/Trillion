import re
from flask import Flask, Blueprint, json, request, render_template, make_response, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user
from flask_login.utils import login_required
from server_controller.user_setting import User
import os

import datetime

main_obj = Blueprint('service', __name__)
acc_obj = Blueprint('account', __name__)

from main import app
# app.config['UPLOAD_FOLDER'] = './'

@main_obj.route('/signin', methods=['GET','POST'])
def signin():
    # username='-'; password='-'
    if request.method =='GET':
        # print('username : ', request.form['username'])
        # print('password : ', request.form['password'])
        if current_user.is_authenticated:
            # session에서 username 추출 및 반환
            print(current_user.username,':',type(current_user.username))
            print(current_user.username,':',type(current_user.username.decode('utf8')))
            username=request.form['username']
            print('TEST1:',username)
            print('TEST2:',current_user.username)
            flag=request.form['flag']
            print('flag :',flag)
            
            return render_template('signin.html', username=username, flag=False)
            # return render_template('signin.html', username=current_user.username.decode('utf8'))
            # return render_template('signin.html', username=current_user.username)
        else:
            return render_template('signin.html', flag=False)

    elif request.method == 'POST':
        # username='-'; password='-'
        username=request.form['username']
        password=request.form['password']
        print('username2 : ', username)
        print('password : ', password)
        # print('direct_flag : ', request.form['direct_flag'])

        # user = User.find(request.form['username'], request.form['password'])
        user = User.examine(username, password)
        if(user == None):
            return render_template('signin.html', warning='아이디 및 비밀번호 오류입니다', remainUser=username, flag=False)
        # elif(user == 'test'):
        #     return render_template('signin.html', warning='존재하지 않는 계정입니다')
        else:
            login_user(user, remember=True, duration=datetime.timedelta(minutes=5))
            # direct_flag=request.form['direct_flag']
            # print(111)
            # if(direct_flag):
            #     logout_user()
        
        # return redirect(url_for('service.signin'))
        # return redirect('/service/signin')
        return render_template('signin.html', username=username, flag=False)

@main_obj.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect('/service/signin')

@main_obj.route('/register', methods=['GET','POST'])
def register():
    if request.method =='GET':
    	return render_template('register.html')

    elif request.method == 'POST':
        print('username : ', request.form['username'])
        print('password : ', request.form['password'])
        
        User.create(request.form['username'], request.form['password'])
        
        return redirect('/service/signin')
        # return redirect(url_for('service.signin'))
        # return make_response(jsonify(success=True), 200)
    
    # return render_template('signin.html')

@main_obj.route('/product', methods=['GET','POST'])
def product():
    # username=request.form['username']
    return render_template('pricing.html')

# --------------------------------------------------------------------

# 테스트 검증 완료
@acc_obj.route('/register_1', methods=['GET','POST']) # 접속할 URL
def register_level_1():
	return render_template('register_1.html')

@acc_obj.route('/register_2', methods=['GET','POST']) # 접속할 URL
def register_level_2():
    return render_template('register_2.html', sort=3, username='-')

# [ id 검증 함수 ]
@acc_obj.route('/examine_id_value', methods=['GET','POST']) # 접속할 URL
def examine_id_value():
    username=request.form['username']
    print('\n\nTTTTTTEST:',username,'\n\n')
    user=User.find(username)
    print(user)
    if(user == None):
        return render_template('register_2.html', sort=1, username=username)
    else:
        return render_template('register_2.html', sort=2, username='-')

@acc_obj.route('/register_3', methods=['GET','POST']) # 접속할 URL
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
            
@acc_obj.route('/register_3_validation', methods=['GET','POST']) # 접속할 URL
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
    return render_template('register_3_validation.html', username=username, password=password, 
                           Patient=Patient, birth=birth, Ward=Ward, Hospital=Hospital, Consultant=Consultant)

@acc_obj.route('/register_4', methods=['GET','POST']) # 접속할 URL
def register_level_4():
    print('level = 4')
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    
    User.create(request.form['username'], request.form['password'])
    return render_template('register_4.html', username=username, password=password)

@acc_obj.route('/complete', methods=['GET','POST']) # 접속할 URL
def register_complete():
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    return render_template('signin.html', username=username, password=password, flag=True)

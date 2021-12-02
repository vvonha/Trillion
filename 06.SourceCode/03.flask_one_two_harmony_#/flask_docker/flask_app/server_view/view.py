from flask import Flask, Blueprint, json, request, render_template, make_response, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user
from flask_login.utils import login_required
from pymysql import NULL
from server_controller.user_setting import User

import os
import re
import datetime
# from main import app

main_obj = Blueprint('service', __name__)
acc_obj = Blueprint('account', __name__)

# from main import app
# app.config['UPLOAD_FOLDER'] = './'
@main_obj.route('/') # 접속할 URL
@main_obj.route('/signin', methods=['GET','POST'])
def signin():
    if request.method =='GET':
        print('@GET :',current_user)
        return redirect(url_for('service.home'))

    elif request.method == 'POST':
        print('@POST :',current_user)
        
        # +++ DB interact code +++
        username=request.form['username']
        password=request.form['password']
        
        # [1] +++ re:TEST +++
        strs = [username, password] # 검증할 문자열
        # p = re.compile('^[a-zA-Z0-9+-_.].{6,}$')
        # p = re.compile('^(?=.*?[a-zA-Z])(?=.*?[0-9]).{6,}$')
        # p = re.compile('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
        # p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        # emails = ['python@mail.example.com', 'python+kr@example.com',
        #         'python-dojang@example.co.kr', 'python_10@example.info',
        #         'python.dojang@e-xample.com',
        #         '@example.com', 'python@example', 'python@example-com']   # 잘못된 형식
        # for s in strs:
        #     print(p.match(s) != None, end=' ')
        #     print()
        
        # [2] +++ Exception +++
        new_s = re.sub(r"[^a-zA-Z0-9]","",username)
        if username!=new_s:
            print('아이디 에러:'+new_s)
            return render_template('signin.html', warning='아이디에 사용 불가능한 문자가 있습니다.', remainUser=username)
        new_s=''
        new_s = re.sub(r"[^a-zA-Z0-9#?!@$%^&*-]","",password) # eliminate +
        if password!=new_s:
            print('패스워드 에러:'+new_s)
            return render_template('signin.html', warning='비밀번호에 사용 불가능한 문자가 있습니다.', remainUser=username)
        
        # for s in strs:
        #     new_s = re.sub(r"[^a-zA-Z0-9]","",s)
        #     if s!=new_s:
        #         print('invalid:'+new_s)
        #         return render_template('signin.html', warning='사용 불가능한 문자가 섞여있습니다.', remainUser=username)
        
        user = User.examine(username, password)
        if(username == ''):
            return render_template('signin.html', warning='아이디를 한 글자 이상 입력해주세요.', remainUser=username)
        
        if(User.find(username) == None and user == None):
            return render_template('signin.html', warning='존재하지 않는 아이디입니다', remainUser=username)
        
        elif(user != None):
            # print('@로그인 성공 =0 (미구현) :',User.set_tryCnt(username))
            login_user(user, remember=True, duration=datetime.timedelta(minutes=5))
            print('@logged in !!')
            
            # Test code (cleaning a cnt)
            warnMsg=User.set_tryCnt(username, True)[0].decode('utf8')
            
            return render_template('signin.html', username=username)
            # return redirect(url_for('service.home'), username=username)
        
        elif(User.find(username) != None):
            warnMsg=User.set_tryCnt(username)[0].decode('utf8')
            if int(warnMsg) >= 5:
                print('잠금')
                return render_template('signin.html', warning='비밀번호 시도 횟수 제한(5회)을 초과하셨습니다.\n관리자에게 문의주세요.(010-9934-9797)', ban=True)
            print('@비밀번호 실패:',warnMsg,'회')
            print(username)
            return render_template('signin.html', warning='비밀번호 실패 %s회. (5회 계정 잠금)'%(warnMsg), remainUser=username)
        
        else:
            return render_template('signin.html', warning='*에러 발생. 조치 필요!', remainUser=username)
        
        # return render_template('signin.html', username=username)

@main_obj.route('/home')
def home():
    print('home :', current_user.is_authenticated)
    if current_user.is_authenticated:
        print('@성공 : 확인 요망 !!')
        print('@username:',current_user.id,':',User.get(current_user.id)) # .decode('ascii')
        print('@username:',current_user.username) # .decode('ascii')
        print('@12.02.TEST:',User.get_user(current_user), User.get_id(current_user))
        return render_template('signin.html', username=current_user.username)
    else:
        return render_template('signin.html')

@main_obj.route('/logout')
def logout():
    logout_user()
    return redirect('/service/signin')

@main_obj.route('/register', methods=['GET','POST'])
def register():
    if request.method =='GET':
    	return render_template('/register/reg_step_1.html')

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
	return render_template('/register/reg_step_1.html')

@acc_obj.route('/register_2', methods=['GET','POST']) # 접속할 URL
def register_level_2():
    return render_template('/register/reg_step_2.html', sort=3, username='-')

# [ id 검증 함수 ]
@acc_obj.route('/examine_id_value', methods=['GET','POST']) # 접속할 URL
def examine_id_value():
    username=request.form['username']
    print('TEST:',username)
    
    # +++ Exception (1) +++  
    new_s = re.sub(r"[^a-zA-Z0-9]","",username)
    if username!=new_s or len(username)<=6:
        print('아이디 에러:'+new_s)
        return render_template('/register/reg_step_2.html', sort=3, username='-')
    
    # +++ Exception (2) +++
    user=User.find(username)
    print(user)
    if(user == None):
        return render_template('/register/reg_step_2.html', sort=1, username=username)
    else:
        return render_template('/register/reg_step_2.html', sort=2, username='-')

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
    return render_template('/register/reg_step_3.html', username=username, password=password)

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
    # file_and_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file_and_path = os.path.join('./', file.filename)
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
    return render_template('/register/reg_step_3_valid.html', username=username, password=password, 
                           Patient=Patient, birth=birth, Ward=Ward, Hospital=Hospital, Consultant=Consultant)

@acc_obj.route('/register_3_validation_2', methods=['GET','POST']) # 접속할 URL
def register_level_3_temp_2():
    
    # request.args.get('username', default = 'bbb', type = str)
    username=request.args.get('username', type = str)
    password=request.args.get('password', type = str)
    temp=request.args.get('temp', type = str)
    
    # print('username : ', request.form['username'])
    # print('password : ', request.form['password'])
    # print('temp : ', request.form['temp'])
    # username=request.form['username']
    # password=request.form['password']
    # temp=request.form['temp']
    
    # with open('test.txt', mode='w') as f:
    #     f.write(temp)
        
    # # Test Code
    # file = request.files['file']
    # # file_and_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # # file_and_path = os.path.join('./', file.filename)
    # file_and_path = os.path.join('./', 'test.txt')
    # file.save(file_and_path)
    # #return 'file uploaded successfully'
    
    # opened_file = open(file_and_path, 'r', encoding='UTF8')
    
    # # test code 2
    # text=''.join(temp.readlines())
    # # text=opened_file.readlines()
    # # print(text)
    
    if "Patient's Name:" in temp:
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
    
    Patient=examine(temp, "Patient's Name:", 100, "Date of birth:")
    birth=examine(temp, "Date of birth:", 100, "Ward:")
    Ward=examine(temp, "Ward:", 100, "Hospital:")
    Hospital=examine(temp, "Hospital:", 100, "Consultant:")
    Consultant=examine(temp, "Consultant:", 100, "\n")
    
    # result(검증 문자열) 추가된 것 확인
    return render_template('/register/reg_step_3_valid.html', username=username, password=password, 
                           Patient=Patient, birth=birth, Ward=Ward, Hospital=Hospital, Consultant=Consultant)

@acc_obj.route('/register_4', methods=['GET','POST']) # 접속할 URL
def register_level_4():
    print('level = 4')
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    
    User.create(request.form['username'], request.form['password'])
    return render_template('/register/reg_step_4.html', username=username, password=password)

@acc_obj.route('/complete', methods=['GET','POST']) # 접속할 URL
def register_complete():
    print('username : ', request.form['username'])
    print('password : ', request.form['password'])
    username=request.form['username']
    password=request.form['password']
    return render_template('signin.html', username=username, password=password)

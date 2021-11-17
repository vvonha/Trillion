import re
import os
from flask import Flask, jsonify, request, render_template, make_response, session, redirect, url_for
from app import texting

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('scan.html')

@app.route('/scan', methods=['GET','POST'])
def scan():
    print('# 스캔 로직 작동중...')
    
    file = request.files['file']
    file_and_path = os.path.join('./', file.filename)
    file.save(file_and_path)
    print('# 업로드 완료...')
    
    # opened_file = open(file_and_path, 'r', encoding='UTF8')
    # text=''.join(opened_file.readlines())
    # text=opened_file.readlines()
    # print(text)
    temp = texting(file_and_path)
    print(temp)
    print('# 텍스팅 처리 완료...')
    
    return redirect('/')

    # if "Patient's Name:" in text:
    #     print('Exist!')
    
    # Patient=examine(text, "Patient's Name:", 100, "Date of birth:")
    # birth=examine(text, "Date of birth:", 100, "Ward:")
    # Ward=examine(text, "Ward:", 100, "Hospital:")
    # Hospital=examine(text, "Hospital:", 100, "Consultant:")
    # Consultant=examine(text, "Consultant:", 100, "\n")
    
    
    # result(검증 문자열) 추가된 것 확인
    # return render_template('/register/reg_step_3_valid.html', username=username, password=password, 
    #                        Patient=Patient, birth=birth, Ward=Ward, Hospital=Hospital, Consultant=Consultant)

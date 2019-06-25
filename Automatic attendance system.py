# -*- coding: cp949 -*-  #한글저장하려면 필요한가 봄

from flask import Flask, render_template, Response, redirect, url_for, request, send_file

from picamera import PiCamera

import pymysql.cursors
import io
import time
import boto3
import json
import os
from datetime import datetime

camera = PiCamera()

camera.resolution = (640 , 480)

app = Flask(__name__)


def get_frame():

    stream = io.BytesIO()

    camera.capture(stream, 'jpeg', use_video_port=True)

    stream.seek(0)

    return stream.read()


@app.route('/')

def main():

    return render_template('index.html')




def gen():

    while True:

        frame = get_frame()

        yield (b'--frame\r\n'

               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/video_feed')

def video_feed():

    return Response(gen(),

                    mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/index', methods = ['POST', 'GET']) 

def index():
        now = datetime.now() #현재 날짜와 시간 가져온다.
        
        if request.method == 'GET': #GET을 받으면 실행


            time.sleep(1) #1초간 대기
        
            camera.capture('/home/pi/Desktop/image.jpg') #찰칵

            time.sleep(1) #1초간 대기

            conn = pymysql.connect(host='localhost',
                    user='phpmyadmin',
                    password='123123',
                    db='phpmyadmin',
                    charset='utf8mb4')  #데이터베이스 연결
            
            fd=open('/home/pi/Desktop/image.jpg', 'rb') #파일을 연다.
            byteBuffer = bytearray(fd.read()) #바이트배열로 받아버린다.
            fd.close() #파일을 닫는다.

            bucket='asd123123'

            for i in range(1, 7 ,1): #중첩 for문 -- 아래 < for faceMatch in response['FaceMatches'] > 포함
                    targetFile= str(i)+".jpg" 
                    #print targetFile -->> 1.jpg 2.jpg ....

                    client=boto3.client('rekognition','us-east-2')

                    try:
                        response=client.compare_faces(SimilarityThreshold=70,      #얼굴비교한다.
                              SourceImage={'Bytes': byteBuffer}, #이미지를 바이트배열로 받는다.
                              TargetImage={'S3Object':{'Bucket':bucket,'Name':targetFile}})
                        
                    except:
                        return render_template('fail.html')  #승인거절 웹 키는 코드

                    

                    for faceMatch in response['FaceMatches']: 
                        #confidence = str(faceMatch['Face']['Confidence']) #문자열로 바꾸는 건데 나중을 위해 지우지 않는다.
                        confidence = faceMatch['Face']['Confidence'] #밑에서 쓰려면 float형으로 받아야 한다.
                        if confidence>95:
                            image = str(i)+".jpg"
                                
                            print(image) #S3에 있는 동일한 사진 확인
                            print(("%.2f" % confidence) + '%' + " 일치") #소수점 2자리까지 나타내려고 수정했다.
                            try:     #데이터베이스 조건문
                                with conn.cursor() as cursor:
                                    sql = 'UPDATE aws SET attendent = %s WHERE picture = %s' # attendent / picture 둘다 문자열로
                                    sql2 = "select * from aws where picture = %s"
                   
                                    cursor.execute(sql, (now, 'https://s3.us-east-2.amazonaws.com/asd123123/' + str(i) +'.jpg')) #위에서 동일한 사진 뽑아내면 동시에 출석부의 attendent 칸에
                                    cursor.execute(sql2, 'https://s3.us-east-2.amazonaws.com/asd123123/' + str(i) +'.jpg')

                                    conn.commit()      # X (출석 안함) 에서 시간 출력 (출석 인증) 으로 변경된다.

                                    rows = cursor.fetchall() #모든행을 배열로 받음.
                                            
                            finally:
                                conn.close()
                                return render_template('result.html',a='https://s3.us-east-2.amazonaws.com/asd123123/'+image,b=rows)  #비교결과 웹 키는 코드

            return render_template('fail.html')  #승인거절 웹 키는 코드                    

       
        
    #return redirect('http://192.168.0.12:5001/aws') #출석부 웹 키는 코드


@app.route('/capture')  #촬영한 이미지를 웹에 띄우는 함수

def capture():

    #camera.capture('/home/pi/Desktop/image.jpg')

    return send_file('/home/pi/Desktop/image.jpg')



@app.route('/result') #결과창 웹 켜주는 함수

def result():

    return render_template('result.html')



@app.route('/aws') #출석부 웹 켜주는 함수

def aws():

    # MySQL Connection 연결
    conn = pymysql.connect(host='localhost', user='phpmyadmin', password='123123',
                           db='phpmyadmin', charset='utf8')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
     
    # SQL문 실행
    sql = "select * from aws"
    curs.execute(sql)
     
    # 데이타 Fetch
    rows = curs.fetchall() #모든행을 배열로 받음.
     
    # Connection 닫기
    conn.close()

    return render_template('aws.html',a=rows)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)  #debug=True



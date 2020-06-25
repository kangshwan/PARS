팀원간 작업 분배  
강승환, 이우림  
raspberry pi-server간 소켓통신 구성  
server에서 django를 이용한 USER interface 구성  
정지원, 신동현  
아두이노, raspberry pi를 이용하여 센서로부터 데이터 수집  
각 센서별 필요한 소프트웨어 개발  
박준섭  
OpenCV를 이용하여 애완동물 구분 소프트웨어 개발

# PARS
Pet Automatic Relief Service

<!-- <p align="center"><img src="" width=""></p> -->

## 프로젝트 개요
- __기획의도__
    - 
- __기능정의__
    - 
- __서버GIT__
    -https://github.com/kangshwan/PARS_SERVER
- __최종보고서__
    -https://github.com/kangshwan/PARS/blob/master/document/IA_%EC%B5%9C%EC%A2%85%EB%B3%B4%EA%B3%A0%EC%84%9C%201%ED%8C%80.pdf
## 개발일지
<details>
<summary> 개발 일지  (눌러서 내용보기) </summary>
<div markdown="1">

## 👩🏽‍💻 6월 11일 (목)
#### To Do
- 깃허브 환경 설정
- Raspberry pi port forwarding
- AWS 서버 파기
- OpenCV를 위한 개발환경 구성
- README.md 페이지 작성
- git remote repo2개 연결하는것 찾아보기
<br>

## 👩🏽‍💻 6월 12일 (금)
#### To Do
- OpenCV를 위한 개발환경 구성
- git remote repo2개 연결하는것 찾아보기
#### Complete
>kang
- 깃허브 환경 설정
- 포트포워딩
- README.md 작성(지속적인 update 예정)
- AWS 서버 생성
<br>

## 👩🏽‍💻 6월 13일 (토)
#### To Do
- OpenCV를 위한 개발환경 구성
- git remote repo2개 연결하는것 찾아보기
- roadcell 2개 동시 제어 방법 찾아보기
- motor를 이용한 사료, 물 통로 on/off 방법 찾아보기
- roadcell에 조건문을 추가하여 효율적인 관리방법 찾아보기
#### Complete
>kang
- git push할 경우 username입력 자동화
>jiwon
- raspberrypi에 roadcell module(aduino)를 연결하여 제어
<br>

## 👩🏽‍💻 6월 14일 (일)
#### To Do

#### Complete
>jiwon
- roadcell module을 통해 언제 얼마나 밥을 먹기 시작하여
  식사가 종료했는지 출력하고 출력데이터 output.txt에 저장
>donghyun
- step motor를 이용하여 먹이를 주는 prototype코드 작성
- 사용자로부터 입력받은 시간에 맞춰 먹이주는 prototype코드 작성
<br>

## 👩🏽‍💻 6월 15일 (월)
#### To Do

#### Complete
>jiwon
- run.py 먹기 시작한 시점, 다 먹은 시점(+ 남았다면 남은 g) 세부 조정
  및 output.txt에 저장
>donghyun
-step motor 이용한 알고리즘 정리 및 입력받은 시간 객체화.
<br>

## 👩🏽‍💻 6월 17일 (수)
#### To Do
- 모터class추가하고 세부조정 필요
- txt파일이 아닌 json파일로 받는것에 대한 논의
- 사용자로부터 먹이줄 무게 받는 func or class 구현
- main파일 완성
#### Complete
>jiwon
- run.py update 서버명령으로 input.txt에 자료저장, 그 자료를 해석하여 먹이를 정해진 시간에 정해진 양 만큼 배급.\
>donghyun
- motor class 추가 및 조정.
- 시간을 받아오는 클래스 및 파일 생성하여 정리.
- main파일 만들어 모든 코드정리.
<br>

## 👩🏽‍💻 6월 18일 (목)
#### To Do
- 모터class추가하고 세부조정 필요
- txt파일이 아닌 json파일로 받는것에 대한 논의
- 사용자로부터 먹이줄 무게 받는 func or class 구현
- main파일 완성
- raspberrypi에서 data읽은 후 jsonfile을 보내기 위하여 class 제작필요
#### Complete
>kang
- django-raspberrypi간에 json file post방식으로 전달 및 django의 sql에 저장.
<br> 

## 👩🏽‍💻 6월 19일 (금)
#### To Do
- 모터class추가하고 세부조정 필요
- txt파일이 아닌 json파일로 받는것에 대한 논의
- 사용자로부터 먹이줄 무게 받는 func or class 구현
- main파일 완성
- raspberrypi에서 data읽은 후 jsonfile을 보내기 위하여 class 제작필요
- camera module raspberrypi에서 streaming
#### Complete
>donghyun
- 사용자로부터 먹이 줄 무게 받는 class 구현(proto type)
- 하는김에 mainpage만들어봄
>jiwon
- run.py에 motor logic을 추가함.
<br>

## 👩🏽‍💻 6월 20일 (토)
#### To Do
- 간단한 device만들어야함
- 먹이를 주는 것에 대한 세부적인 조정이 필요
- server쪽과 주고받을 파일을 어떻게 할것인가에 대해 논의 필요
- 강아지 등록 추가, 우리개 template에서 등록된 강아지 list하고 각 강아지별 식사량 확인.
- 원하는 시간대를 raspberrypi로 전송하여 시간에 맞춰서 동작하도록 함
#### Complete
>jiwon
- run.py에 motor logic을 추가함
<br>

## 👩🏽‍💻 6월 21일 (금)
#### To Do
- 간단한 device만들어야함
- 먹이를 주는 것에 대한 세부적인 조정이 필요
- server쪽과 주고받을 파일을 어떻게 할것인가에 대해 논의 필요
~~- 강아지 등록 추가, 우리개 template에서 등록된 강아지 list하고 각 강아지별 식사량 확인.~~
- 원하는 시간대를 raspberrypi로 전송하여 시간에 맞춰서 동작하도록 함
- 마지막으로 django server 배포
## 참고 자료
<!-- - []() -->


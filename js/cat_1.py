import cv2
import numpy as np
#얼국 인식용 xml 파일 
face_classifier = cv2.CascadeClassifier('../opencv_build/opencv/data/haarcascades/haarcascade_frontalcatface.xml')

#전체 사진에서 얼굴 부위만 잘라 리턴
def face_extractor(img):
    #흑백처리 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #얼굴 찾기 
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    #찾은 얼굴이 없으면 None으로 리턴 
    if faces is():
        return None
    #얼굴들이 있으면 
    for(x,y,w,h) in faces:
        #해당 얼굴 크기만큼 cropped_face에 잘라 넣기 
        #근데... 얼굴이 2개 이상 감지되면??
        #가장 마지막의 얼굴만 남을 듯
        cropped_face = img[y:y+h, x:x+w]
    #cropped_face 리턴 
    return cropped_face

#카메라 실행 
cap = cv2.VideoCapture(0)
#저장할 이미지 카운트 변수 
count = 0
while True:
    #카메라로 부터 사진 1장 얻기 
    ret, frame = cap.read()
    #얼굴 감지 하여 얼굴만 가져오기 
    if face_extractor(frame) is not None:
        count+=1
        #얼굴 이미지 크기를 200x200으로 조정 
        face = cv2.resize(face_extractor(frame),(200,200))
        #조정된 이미지를 흑백으로 변환 
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        #faces폴더에 jpg파일로 저장 
        # ex > faces/user0.jpg   faces/user1.jpg ....
        file_name_path = 'faces/user'+str(count)+'.jpg'          
        cv2.imwrite(file_name_path,face)
        
        #화면에 얼굴과 현재 저장 개수 표시          
        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Face Cropper',face)
    else:
        print("Face not Found")
        pass

    if cv2.waitKey(1)==13 or count==100:
        break

cap.release()
cv2.destroyAllWindows()
print('Colleting Samples Complete!!!')
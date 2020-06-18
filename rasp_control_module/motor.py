import time
import sys 
import RPi.GPIO as GPIO
import Gettime
        
now = time.localtime()
#시간 나누어놓은 파일을 여기에 import해야함. time_save라는 파일로.
class motor:
    def __init__(self,get_time):
        self.time = []
        self.time = get_time
        self.now = time.localtime()
    
    def food_trunk(self):
        GPIO.setmode(GPIO.BCM) #GPIO 세팅
        StepPins = [19,17,18,16] #GPIO번호(BCM) 17,22,23,24 physical 11,15,16,18

        for pin in StepPins:
            print("Setup pins")
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

        Seq = [[0,0,0,1],
               [0,0,1,0],
               [0,1,0,0],
               [1,0,0,0]]  #step모터가 돌아갈 sequence 설정. 4part로 나눠 90도씩 돌아가게 설정. 

        StepCount = len(Seq)
        StepCounter = 0
        #StepDir = 1 # 1일때 시계방향으로 돌아감. #방향제어 필요할시 loop에 추가할 것.
        if (self.time[0] == now.tm_mon and self.time[1] == now.tm_mday and self.time[2] == now.tm_hour):
            print(StepCounter)
            print(Seq[StepCounter]) #두 줄을 통해 Stepcounter 와 Sequence의 관계 및 역할 알 수 있음
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq[StepCounter][pin] != 0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
                StepCounter += 1
                time.sleep(60)
                
                if(StepCounter < 0):
                    StepCounter = StepCount    
                    
                if(StepCounter == StepCount):
                    i = 0
                    print("Ran out of foods.")  #문제점 4번 다돌리기전 음식채우면 어떡하냐, 
        
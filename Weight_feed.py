import time
import sys 
import RPi.GPIO as GPIO

EMULATE_HX711=False
referenceUnit = 1 

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(120)
hx.reset()
hx.tare()

print("Tare done! Add weight now...")
now = time.localtime() #글로벌 시간 호출함수
class check_weight:
    val = 0
    val_list = []
    val_list_dif = []
    now = time.localtime()
    i = 0
    while True:
        try:
            val = hx.get_weight(5)
            print("current weight is")
            print(val)
            val_list.append(val)
            print("val_list is")
            print(val_list)
            print("current time is")
            print("%02d/%02d %02d:%02d:%02d" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
            if len(val_list) >= 2:
                val_list_dif.append(val_list[i] - val_list[i+1])
            if val_list_dif[i] >=10:
                print("your pet is eating")
            elif val_list_dif[i] <= 1 and val_list[i-1] > val_list[i]:
                print("your pet has finishing eating")
            else:
                pass
            i += 1
            print("val_list_dif is")
            print(val_list_dif)
            hx.power_down()
            hx.power_up()
            time.sleep(3)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

#시간설정파트 사용자가 입력을 하면 서버로부터 그 값을 받아올것. day,hour,min 만 현재 염두중.
class feed_timeset:
    time_save = list()
    i = 0

    def __init__(self, day, hour, min):
        self.day = day
        self.hour = hour
        self.min = min
    
    def get_time(self):
        time_save.insert(i, [self.day, self.hour, self.min])
        
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
        StepDir = 1 # 1일때 시계방향으로 돌아감. #방향제어 필요할시 loop문에 추가할 것.
        i = 0
        try:
            if (time_save[i][0] == now.tm_mon and time_save[i][1] == now.tm_mday and time_save[i][2] == now.tm_hour):
                print(StepCounter)
                print(Seq[StepCounter]) #두 줄을 통해 Stepcounter 와 Sequence의 관계 및 역할 알 수 있음

                for pin in range(0, 4):
                    xpin = StepPins[pin]
                    if Seq[StepCounter][pin] != 0: #Seq[][] 0이 아니면 동작
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                StepCounter += 1
                if(StepCounter < 0):
                    StepCounter = StepCount
                if(StepCounter == StepCount):
                    print("Ran out of foods.")
                    break
        except KeyboardInterrupt:   
            GPIO.cleanup()
import time
import sys 
import RPi.GPIO as GPIO
import json

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

val_list = []
val_list_dif = []
output_list = []
now = time.localtime()

i = 0
j = 0
k = 0

while True:
    try:
        val = hx.get_weight(5)
        print(val)
	val_list.append(val)
	f = open('output.txt', 'a')
	if len(val_list) >= 2:
		val_list_dif.append(val_list[i] - val_list[i+1])
		print(val_list_dif)
		print("val_list_dif")
		if val_list_dif[i] >= 10 and j == 0:
			f.write(("%02d/%02d %02d:%02d start eating\n" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)))
			print("%02d/%02d %02d:%02d start eating" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min))
			j += 1
			k += 1				
		if -2 <= val_list_dif[i] <= 2:
			if val_list[i-1] >= val_list[i]:
				if val_list[i] < 5 and k == 1:		
					f.write(("%02d/%02d %02d:%02d finish eating\n" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)))
					print("%02d/%02d %02d:%02d finish eating" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min))
					j -= 1
					k -= 1
				if 5 <= val_list[i] <=189 and k == 1:
					f.write(("%02d/%o2d %02d:%02d finish eating but %dg left\n" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, val_list[i])))
					print("%02d/%02d %02d:%02d finish eating but %dg left" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min,val_list[i]))
					j -= 1
					k -= 1
		else:
			pass
        i += 1  #이게 if문 안에 있는지 밖에있는지?
        hx.power_down()
        hx.power_up()
        time.sleep(1)
	i += 1
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()	

#시간설정파트 사용자가 입력을 하면 서버로부터 그 값을 받아올것. day,hour,min 만 현재 염두중.
#사용자로부터 time file로 시간 받기
with open('user_set_time') as f:
    inventory = json.load(f)
inventory
    
time_save = list()
"""
def get_time(day, hour, min):
    i = 0
    for i in range (0, 4):
        time_save.insert(i, [day, hour, min])
        i+=1
        print(time_save)
""" #필요없을듯

"""
def openfile():
    f = open("new_file.txt", 'w')
    for i in range(0, 5):
        data = "%d users_setting_time:05:12:16:\n" %i   #05일 12시 16분
        f.write(data)
        f.close()
"""

def readlines_obo():
    f = open("new_file.txt",'r')
    lines = f.readlines()
    for line in lines:
        print(line)
    f.close()
    print(type(lines))
    print(len(lines))
#파일을 사용자로부터 받아서 열고 읽음 1줄씩 그리고 한줄씩 리스트에 정리됨.

def split_time(self,):
    Users_timeset = lines[].split(':')
    print(Users_timeset)
    Real_users_timeset = Users_timeset[1:4]
    print(Real_users_timeset)
#리스트를 : 를 기준으로 day, hour, min 기준으로 나눔.

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
    StepDir = 1 # 1일때 시계방향으로 돌아감. #방향제어 필요할시 loop에 추가할 것.
    i = 0
    while 1:
        if (time_save[i][0] == now.tm_mon and time_save[i][1] == now.tm_mday and time_save[i][2] == now.tm_hour):
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
        
    if __name__ == "__main__":
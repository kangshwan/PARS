#! /usr/bin/python2
#-*-coding:utf-8-*-
import time
import sys
import wiringpi as wp
now = time.localtime()
PIN_1A = 27
PIN_1B = 0
PIN_2A = 1
PIN_2B = 24
EMULATE_HX711=False
wp.wiringPiSetup()
wp.pinMode(PIN_1A, 1)
wp.pinMode(PIN_1B, 1)
wp.pinMode(PIN_2A, 1)
wp.pinMode(PIN_2B, 1)
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

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
hx.set_reference_unit(120)
#hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()
val_list = [] #현재값들의 리스트 즉 sudo python run.py실행하고부터의val값들의list
val_list_dif = []#현재값과다음값의차이들의 리스트

i = 0
j = 0
k = 0
q = 0
cur_food = False
#from_time = time from server  
def rotate():
	wp.pinMode(PIN_1A, 1)
	wp.pinMode(PIN_1B, 1)
	wp.pinMode(PIN_2A, 1)
	wp.pinMode(PIN_2B, 1)
	wp.digitalWrite(PIN_1A, 1)
    	wp.digitalWrite(PIN_1B, 0)
    	wp.digitalWrite(PIN_2A, 0)
    	wp.digitalWrite(PIN_2B, 0)
    	time.sleep(0.1)
    	wp.digitalWrite(PIN_1A, 0)
    	wp.digitalWrite(PIN_1B, 1)
    	wp.digitalWrite(PIN_2A, 0)
    	wp.digitalWrite(PIN_2B, 0)
    	time.sleep(0.1)
    	wp.digitalWrite(PIN_1A, 0)
    	wp.digitalWrite(PIN_1B, 0)
    	wp.digitalWrite(PIN_2A, 1)
    	wp.digitalWrite(PIN_2B, 0)
    	time.sleep(0.1)
    	wp.digitalWrite(PIN_1A, 0)
    	wp.digitalWrite(PIN_1B, 0)
    	wp.digitalWrite(PIN_2A, 0)
    	wp.digitalWrite(PIN_2B, 1)
    	time.sleep(0.1)
while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)  #현재값
	#get_val = 먹이를몇그램줘야하는지를서버에서text파일로보내주면그값을읽을예정필히추가해야함
        print(val)
	from_val = #서버에서호출한밥의양혹은설정한밥의양
	if from_time: #서버에서 호출한 시간이 되면
		if val < from_val:#현재값이 서버에서 요구한값보다 작다면180도 돌려라 
			if cur_food == False:
				for i in range(6):
					rotate()
				cur_food = True #cur_food값 false ㅡ> true
			else:
				pass
	if val >= from_val:#만약 현재값이 서버에서 요구한값보다 크다면 180도 돌려라
		if cur_food == True
			for i in range(6):
				rotate()
			cur_food = False
	val_list.append(val)
	f = open('output.txt', 'a')
	g = open('input.txt', 'r') #input.txt는서버에서받아올파일
	a = ("%02d:%02d"%(now.tm_hour, now.tm_min))#현재시간 시간 분추후초도추가할 예정
	text_context_list=[] #input.txt의내용을한줄마다리스트에추가
	line_num = 1 #input.txt의 첫번째줄두번째줄을뽑기위한변수
	line_data = g.readline()#한줄읽기
	while line_data:#한줄한줄읽으면서text_contect_list에추가
		line_data=g.readline()
		text_contect_list.append(line_data)
		line_num += 1
	g.close()
	#for q in range(len(text_contect_list)):#text_contect_list의길이만큼for문을돌려서
	#	if a == text_contect_list[q]:#만약현재시간분초가리스트에있는시간분초와 같다면
	#		if val <= 300:#만약현재무게가text에서받아온값보다작다면
	#			classname.foodstart()#모터를돌려서먹이가나온다
					       	     
	#		if val > 300:#만약현재무게가tex에서받아온값보다크다면
	#			classname.foodstop()#모터를돌려서먹이안나오게한다.
	#		else:
	#			pass #else 패스

	if len(val_list) >= 2: #val_list길이가2이상일떄부터
		val_list_dif.append(val_list[i] - val_list[i+1]) #차이값들을 리스트로저장
		
		print(val_list_dif)	
		if val_list_dif[i] >= 10 and j == 0:#차이가10이상이면밥을먹기시작
			f.write(("%02d/%02d %02d:%02d start eating\n" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)))
			print("%02d/%02d %02d:%02d start eating" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min))
			j += 1 #j,k값들의 값을 0,1왔다갔다하면서on,off
			k += 1				
		if -2 <= val_list_dif[i] <= 2:#만약디프런스가미세하다면다먹었다호출해주고
			if val_list[i-1] >= val_list[i]:
				if val_list[i] < 5 and k == 1:#무게가 5g이하먄 다먹음		
					f.write(("%02d/%02d %02d:%02d finish eating\n" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)))
					print("%02d/%02d %02d:%02d finish eating" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min))
					j -= 1
					k -= 1
				if 5 <= val_list[i] <=189 and k == 1:#무게가처음준무게와5사이면몇g남음
					f.write(("%02d/%o2d %02d:%02d finish eating but %dg left\n" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, val_list[i])))
					print("%02d/%02d %02d:%02d finish eating but %dg left" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min,val_list[i]))
					j -= 1
					k -= 1
		else:
			pass
		i += 1

	f.close()
        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(1)
		
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

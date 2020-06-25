#! /usr/bin/python2
#-*-coding:utf-8-*-
import time
import sys
import wiringpi as wp
import requests  
import json
import socket_send

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
start_val=0
before_val = 0
max_val=0
fin_val = 0
send_val = 0
eat_count=0
is_max = False
is_eating = False
ready_to_send = False
food_on=True
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
start_val=hx.get_weight(5)
start_val = 0-start_val
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
		val = 0-val
		val -= start_val
		if val <= 0:
			val = 0
		print(val)
		if (val != 0 and (before_val == val or (before_val - val)<1) and before_val > max_val):
			max_val = before_val	
			is_max = True
		print("MAXVAL:" ,max_val)
		if(is_max and before_val - val > 3):
			is_eating = True
		if(is_eating and before_val == val):
			if eat_count < 3:
				eat_count +=1
			else:
				print("냠냠 다먹었다")
				fin_val = val
				send_val = max_val - fin_val
				max_val = 0
				fin_val = 0
				is_eating = False
				eat_count = 0
				ready_to_send = True
				is_max = False
				print(send_val)
		if ready_to_send:
			send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
			url = "http://ec2-13-209-7-55.ap-northeast-2.compute.amazonaws.com:8080/dogfeed/ourdog/"
			data = {'data':{'name':'뽀삐','weight':send_val, 'time': send_time}}
			headers = {'content-type': 'application/json'}
			r=requests.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
			print(r)
			ready_to_send = False
		hx.power_down()
		hx.power_up()
		time.sleep(1)
		before_val = val
	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()

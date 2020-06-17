#! /usr/bin/python2

import time
import sys

now = time.localtime()

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
val_list = []
val_list_dif = []
output_list = []

i = 0
j = 0
k = 0
while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)
	get_val = classname.get_weight(??)
        print(val)
	val_list.append(val)
	f = open('output.txt', 'a')
	g = open('input.txt', 'r', encoding='UTF-8')
	a = ("%02d:%02d"%(now.tm_hour, now.tm_min))
	text_context_list=[]
	line_num = 1
	line_data = g.readline()
	while line_data:
		line_data=g.readline()
		text_contect_list.append(line_data)
		line_num += 1
	g.close()
	for i in range(len(line_data)):
		if a == text_contect_list[i]:
			if val <= get_val:
				classname.foodstart() #foodweight를초기설정으로 지정해서 그val(무게)가
					       	       #초기설정을 넘어가면 foodstop()
			else if val > get_val:
				classname.foodstop()
			else:
				pass 

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

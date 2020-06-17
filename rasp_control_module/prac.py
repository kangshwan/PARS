#! /usr/bin/python2
import time
import sys
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

now = time.localtime()

EMULATE_HX711=False

referenceUnit = 1

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()
#For windows.

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

#만약 로드셀을 실행했을때 값이 이상하다면 hx.set_reference_Unit(referenceUnit)에서 #을 없애주고 바로윗줄 코드 주석처리 필요.
#그 후 무게를 아는 물건의 무게를 로드셀로 측정(여러번 해야함!!) 그 값들의 평균을 실제 물건의 무게로 나누어 나온 정수를 첫째줄 ( ) 안에 넣으면 됩니다.
hx.set_reference_unit(120)
#hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

#로드셀 2개 쓰고 싶을때는 이걸 사용하면 될 것 같습니다.
#hx.tare_A()
#hx.tare_B()
val_list = [] #현재값들의 리스트 즉 sudo python run.py실행하고부터의val값들의list
val_list_dif = []#현재값과다음값의차이들의 리스트

i = 0
j = 0
k = 0
q = 0 
while True:
    try:
        val = hx.get_weight(5)  #현재값
	#get_val = 먹이를몇그램줘야하는지를서버에서text파일로보내주면그값을읽을예정필히추가해야함
        print(val)
	val_list.append(val)
	f = open('output.txt', 'a')
	g = open('input.txt', 'r', encoding='UTF-8') #input.txt는서버에서받아올파일
	a = ("%02d:%02d"%(now.tm_hour, now.tm_min))#현재시간 시간 분추후초도추가할 예정
	text_context_list=[] #input.txt의내용을한줄마다리스트에추가
	line_num = 1 #input.txt의 첫번째줄두번째줄을뽑기위한변수
	line_data = g.readline()#한줄읽기
	while line_data:#한줄한줄읽으면서text_contect_list에추가
		line_data=g.readline()
		text_context_list.append(line_data)
		line_num += 1
	g.close()
	for q in range(len(text_context_list)):#text_context_list의길이만큼for문을돌려서
		if a == text_context_list[q]:#만약 현재시간분초가 리스트에있는 시간분초와 같다면
			if val <= get_val:#만약현재무게가text에서받아온값보다작다면
				classname.foodstart()#모터를돌려서먹이가나온다		       	     
			else if val > get_val:#만약현재무게가tex에서받아온값보다크다면
				classname.foodstop()#모터를돌려서먹이안나오게한다.
			else:
				pass #else 패스

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
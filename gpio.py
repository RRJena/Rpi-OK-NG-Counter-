import RPi.GPIO as GPIO
import time
OK=0
NG=0
input_pin1=16
input_pin2=12
input_pin3=26
output_pin1=20
output_pin2=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin1, GPIO.IN)
GPIO.setup(input_pin2, GPIO.IN)
GPIO.setup(input_pin3, GPIO.IN)
GPIO.setup(output_pin1, GPIO.OUT)
GPIO.setup(output_pin2, GPIO.OUT)     
try:
    while True:
        d1=0
        d0=0
        in1=GPIO.input(input_pin1)
        in2=GPIO.input(input_pin2)
        in3=GPIO.input(input_pin3)
        while in1==0:
            print("OK Loop")
            in1=GPIO.input(input_pin1)
            in3=GPIO.input(input_pin3)
            if in1==1:
                OK+=1
            if in3==0:
                d0+=1
            if in3==1:
                if d0>=1:
                    NG+=1
                    d0=0
            print("d0:"+str(d0))
            print(OK, NG)
            
        while in3==0:
            print("In NG Loop")
            in3=GPIO.input(input_pin3)
            in1=GPIO.input(input_pin1)
            if in3==1:
                NG+=1
            if in1==0:
                d1+=1
            if in1==1:
                if d1>=1:
                    OK+=1
                    d1=0
            print("d1:"+str(d1))
            print(OK, NG)             
        print(OK, NG)
        
        #print(in1,in2,in3)
        #time.sleep(1)
except:
    print("GPIO Error")
finally:
    GPIO.cleanup()

from flask import Flask, render_template,request
import time
import pigpio
import RPi.GPIO as GPIO
from gpiozero import PWMLED
from gpiozero import LED
from multiprocessing import Process
#-------<馬達控制區L298N>
l298n2 = PWMLED(2)
l298n3 = PWMLED(3)
l298n4 = PWMLED(4)
l298n17 = PWMLED(17)
pin=[l298n2,l298n3,l298n4,l298n17]
for i in pin:
    i.value = 0
n1 = [0,0,0,0] #紀錄前後左右狀態
#-------</馬達控制區L298N>

#-------<傳感器HC-SR04>
led1=LED(20)
TRIGGER_PIN = 12
ECHO_PIN = 16
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
 
GPIO.output(TRIGGER_PIN, GPIO.LOW)
#-------</傳感器HC-SR04>
def hc04():
    global TRIGGER_PIN,ECHO_PIN,distance
    global led1,n1,pin
    while True:
            GPIO.output(TRIGGER_PIN, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(TRIGGER_PIN, GPIO.LOW)
            while GPIO.input(ECHO_PIN) == 0:
                start_time = time.time()
            while GPIO.input(ECHO_PIN) == 1:
                end_time = time.time()
            etime = end_time - start_time
            distance = 17150 * etime
            print('距離為 {:.1f} 公分'.format(distance))
            time.sleep(1)
            if int (distance)<20:
                led1.on()
            else:
                led1.off()
#-------<傳感器HC-SR04 code>

#-------</傳感器HC-SR04 code>

#-------<轉舵MG90S>
pin_servo = 27
# 启动服务
# sudo systemctl start pigpiod
# 停止运行服务
# sudo systemctl stop pigpiod
# 将服务设置为开机启动
# sudo systemctl enable pigpiod
# 将服务设置为禁止开机启动
# sudo systemctl disable pigpiod
GPIO.setmode(GPIO.BCM)
pwm = pigpio.pi()
pwm.set_mode(pin_servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(pin_servo, 50)  # 50Hz frequency
#-------</轉舵MG90S>

#-------<轉舵定義>
def destroy():
    pwm.set_PWM_dutycycle(pin_servo, 0)
    pwm.set_PWM_frequency(pin_servo, 0)
def setDirection(angle):
    duty = 500 + (angle / 180) * 2000
    pwm.set_servo_pulsewidth(pin_servo, duty)
    print("角度=", angle, "-> duty=", duty)
#-------</轉舵定義>


def left():
    global n1
    n1 = ch1(2,n1)
    ch2(n1)
    setDirection(70)
    return render_template('index.html')
def middle():
    setDirection(90)
    return render_template('index.html')
def right():
    global n1
    n1 = ch1(3,n1)
    ch2(n1)
    setDirection(120)
    return render_template('index.html') 
   
#-------<馬達控制區L298N-定義>
def ch1(i,n1): #無狀態
    if int(i)==0:
        n1[1]=0
    elif int(i)==1:
        n1[0]=0
    elif int(i)==2:
        n1[3]=0
    elif int(i)==3:
        n1[2]=0
    n1[i] = 1
    return n1
def ch2(n1):
    if n1==[1,0,1,0] : #前左
        pin[0].value = 0
        pin[1].value = 0.50
        pin[2].value = 0.75
        pin[3].value = 0
        print("前左")
    elif n1==[1,0,0,1] : #前右
        pin[0].value = 0
        pin[1].value = 0.75
        pin[2].value = 0.50
        pin[3].value = 0
        print("前右")
    elif n1==[0,1,1,0] : #後左
        pin[0].value = 0.50
        pin[1].value = 0
        pin[2].value = 0
        pin[3].value = 0.75
        print("後左")
    elif n1==[0,1,0,1] : #後左
        pin[0].value = 0.75
        pin[1].value = 0
        pin[2].value = 0
        pin[3].value = 0.50
        print("後右")
    elif n1==[0,0,0,0]:
        pin[0].value = 0
        pin[1].value = 0
        pin[2].value = 0
        pin[3].value = 0
#-------</馬達控制區L298N-定義>

#-------<網站架區>
app = Flask(__name__)
@app.route('/')
def main():
    return render_template('index.html')
@app.route('/left')
def left():
    global n1
    n1 = ch1(2,n1)
    ch2(n1)
    setDirection(70)
    return render_template('index.html')
@app.route('/middle')
def middle():
    setDirection(90)
    return render_template('index.html')
@app.route('/right')
def right():
    global n1
    n1 = ch1(3,n1)
    ch2(n1)
    setDirection(120)
    return render_template('index.html')
@app.route('/run')
def run():
    global n1
    n1 = ch1(0,n1)
    ch2(n1)
    pin[0].value = 0
    pin[1].value = 0.75
    pin[2].value = 0.75
    pin[3].value = 0
    print(n1)
    return render_template('index.html')
@app.route('/back')
def back():
    global n1
    n1 = ch1(1,n1)
    ch2(n1)
    pin[0].value = 0.75
    pin[1].value = 0
    pin[2].value = 0
    pin[3].value = 0.75
    print(n1)
    return render_template('index.html')
@app.route('/stop')
def stop():
    global n1
    n1=[0,0,0,0]
    pin[0].value = 0
    pin[1].value = 0
    pin[2].value = 0
    pin[3].value = 0
    return render_template('index.html')
#-------</網站架區>

#--------<執行區>
if __name__ == '__main__':
    try:
        p = Process(target=hc04) #多核心處理(同時處理多程式) target=函式 args=函數的輸入值 例:hc04(這裡的值)
        p.start()   #開始區
        app.run(host='0.0.0.0', port=8080,debug=True,use_reloader = False)
        p.join()  #結束
    finally:
        GPIO.cleanup()
        print("關閉程式")
#--------</執行區>  
from machine import Pin, PWM
from servo import Servo
import time
from machine import UART
import json


time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上
servo_yaw = Servo(1)
servo_yaw.set_angle(0)
time.sleep(2)
flag = 1

#_thread.start_new_thread(run,("1",)) #开启线程1,参数必须是元组
#_thread.start_new_thread(step_yaw,("2",)) #开启线程2，参数必须是元组

while True:

    servo_yaw.set_angle_relative(flag * 0.1)
    

        



from machine import Pin, PWM
from servo import Servo
import time
from machine import UART
import json

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上

servo_yaw = Servo(0)
servo_pitch = Servo(1)



servo_pitch.set_angle_relative()
from machine import Pin, PWM
from servo import Servo
import time
from machine import UART
import json
import _thread

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上

servo_yaw = Servo(1, limit_min_angle = 90-50, limit_max_angle = 90+50)
servo_pitch = Servo(0, limit_min_angle = 90-18, limit_max_angle = 90+45)

uart = UART(1, 115200, rx=21, tx=20)  # 设置串口号1和波特率

kp_yaw = 0.0009
kp_pitch = 0.0009

yaw_ = 0
pitch_ = 0

def receive(callback):
    global yaw_, pitch_
    while True:
        # 判断有无收到信息
        if uart.any():
            time.sleep(0.01)
            json_data = uart.read(uart.any())  # 接收可用数据
            try:
                # 解码并分割数据
                data = json.loads(json_data)  # 解析 JSON 字符串为字典
                yaw = data['yaw']  # 提取 yaw 值
                pitch = data['pitch']  # 提取 pitch 值
                print(f'Parsed Yaw: {yaw}, Parsed Pitch: {pitch}')  # 打印解析后的值
                yaw_ = yaw * kp_yaw
                pitch_ = pitch * kp_pitch
                

            except ValueError as e:
                print(f"数据格式错误: {e}")  # 捕获并打印格式错误
            except IndexError:
                print("接收到的数据格式不正确，无法提取 yaw 和 pitch。")
            
def servo_move(callback):
    while True:
        servo_yaw.set_angle_relative(yaw_)  # 设置舵机角度
        servo_pitch.set_angle_relative(pitch_)  # 设置舵机角度

_thread.start_new_thread(receive,("1",))
_thread.start_new_thread(servo_move,("2",))










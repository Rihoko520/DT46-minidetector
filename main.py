from machine import Pin, PWM
from servo import Servo
import time
from machine import UART
import json

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上

servo_yaw = Servo(0)
servo_pitch = Servo(1)

uart = UART(1, 115200, rx=21, tx=20)  # 设置串口号1和波特率

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
            servo_yaw.set_angle(yaw)  # 设置舵机角度
            servo_pitch.set_angle(pitch)  # 设置舵机角度

            # 发送反馈信息
            uart.write(f'{yaw}/{pitch}\n'.encode('utf-8'))  # 发送一条数据

        except ValueError as e:
            print(f"数据格式错误: {e}")  # 捕获并打印格式错误
        except IndexError:
            print("接收到的数据格式不正确，无法提取 yaw 和 pitch。")


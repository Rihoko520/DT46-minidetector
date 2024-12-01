import serial
import time
import json


class Trans():
    def __init__(self, serial_port = '/dev/ttyACM1', baud_rate = 115200, timeout = 1):
        self.ser = serial.Serial(serial_port, baud_rate, timeout = timeout)
        # 等待串口稳定
        time.sleep(2)
    def send(self, yaw, pitch):
        yaw_pitch = {'yaw': yaw, 'pitch': pitch}
        json_data = json.dumps(yaw_pitch)  # 将字典转换为 JSON 字符串
        self.ser.write((json_data + '\n').encode('utf-8'))  # 发送 JSON 字符串

    def close(self):
        # 关闭串口
        self.ser.close()
        print("串口已关闭")
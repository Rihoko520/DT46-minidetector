from machine import Pin, PWM
from servo import Servo
import time
from machine import UART
import json
import _thread
from pid import PIDController

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上
class Aim():
    def __init__(self):
        self.yaw = 0
        self.pitch = 0
        
        self.yaw_current = 0
        self.pitch_current = 0        
       
        self.yaw_input = 0
        self.pitch_input = 0

        self.pid_yaw = PIDController(Kp=0.215, Ki=0, Kd=0)
        self.pid_pitch = PIDController(Kp=0, Ki=0, Kd=0)

        self.servo_yaw = Servo(1, limit_min_angle = 90-50, limit_max_angle = 90+50)
        self.servo_pitch = Servo(0, limit_min_angle = 90-18, limit_max_angle = 90+45)

        self.uart = UART(1, 115200, rx=21, tx=20)  # 设置串口号1和波特率
    
    def receive(self, callback):
        while True:
            # 判断有无收到信息
            if self.uart.any():
                time.sleep(0.008)
                json_data = self.uart.read(self.uart.any())  # 接收可用数据
                try:
                    # 解码并分割数据
                    data = json.loads(json_data)  # 解析 JSON 字符串为字典
                    self.yaw = data['yaw']  # 提取 yaw 值
                    self.pitch = data['pitch']  # 提取 pitch 值
                    #print(f'Parsed Yaw: {self.yaw}, Parsed Pitch: {self.pitch}')  # 打印解析后的值
                    
                except ValueError as e:
                    print(f"数据格式错误: {e}")  # 捕获并打印格式错误
                except IndexError:
                    print("接收到的数据格式不正确，无法提取 yaw 和 pitch。")
                
    def servo_move(self, callback):
        while True:
            self.yaw_input = self.pid_yaw.update(self.yaw, self.yaw_current)
            yaw_targe_angle_last = self.servo_yaw.targe_angle
            print(self.yaw_input)
            
            self.pitch_input = self.pid_pitch.update(self.pitch, self.pitch_current)
            pitch_targe_angle_last = self.servo_pitch.targe_angle
            print(self.pitch_input)
            
            self.servo_yaw.set_angle_relative(self.yaw_input)  # 设置舵机角度
            self.yaw_current = self.servo_yaw.targe_angle - yaw_targe_angle_last

            self.servo_pitch.set_angle_relative(self.pitch_input)  # 设置舵机角度
            self.pitch_current = self.servo_pitch.targe_angle - pitch_targe_angle_last
            
    def start(self):
        _thread.start_new_thread(self.receive,("1",))
        _thread.start_new_thread(self.servo_move,("2",))
        
aim = Aim()
time.sleep(2)
aim.start()
        











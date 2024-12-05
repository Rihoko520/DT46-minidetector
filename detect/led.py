'''
实验名称:LED闪烁
实验平台:核桃派
'''

#导入相关模块
import board,time
from digitalio import DigitalInOut, Direction

#构建LED对象和初始化
led = DigitalInOut(board.LED) #定义引脚编号
led.direction = Direction.OUTPUT  #IO为输出

while True:

    led.value = 1 #输出高电平，点亮板载LED蓝灯
    
    time.sleep(0.5)
    
    led.value = 0 #输出低电平，熄灭板载LED蓝灯
    
    time.sleep(0.5)
    
    print("Hello WalnutPi!") #输出打印信息
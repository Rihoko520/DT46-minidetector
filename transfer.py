import serial
import time
import json
# 配置串口参数
serial_port = '/dev/ttyACM1'  # 根据实际情况修改
baud_rate = 115200       # 波特率
timeout = 1            # 超时设置

# 创建串口对象
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

# 等待串口稳定
#time.sleep(2)
i = 0
yaw = 20
pitch = 90
# 打包为 JSON 格式
data = {
    'yaw': yaw,
    'pitch': pitch
}

json_data = json.dumps(data)  # 将字典转换为 JSON 字符串

try:
    while True:
        ser.write((json_data + '\n').encode('utf-8'))  # 发送 JSON 字符串
        i += 1

        time.sleep(0.1)

        if ser.in_waiting > 0:  # 检查是否有数据可读
            response = ser.read(ser.in_waiting)  # 读取所有可用数据
            print(f'Received: {response.decode()}')

except KeyboardInterrupt:
    print("程序被用户中断")

finally:
    # 关闭串口
    ser.close()
    print("串口已关闭")
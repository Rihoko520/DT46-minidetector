import cv2  # 导入 OpenCV 库
import time  # 导入时间库
from detector import ArmorDetector  # 从 detector 导入 Detector 类
from transfer import Trans
from armor_tracker_node import ArmorTracker
from loguru import logger
import time

class Cam():
    def __init__(self, cam_params):    
        self.width = cam_params["width"]  # 你想要的宽度
        self.height = cam_params["height"]   # 你想要的高度
        self.fps = cam_params["fps"]  # 你想要的帧率
        self.cam_num = cam_params["cam_num"]
    def detect(self, detector, tracker, transfer):
        tracker.pic_width = self.width
        video_stream = cv2.VideoCapture(self.cam_num)  # 打开视频流
                # 设置分辨率
        video_stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        video_stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        video_stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        # 设置帧率
        video_stream.set(cv2.CAP_PROP_FPS, self.fps)
        w = video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = video_stream.get(cv2.CAP_PROP_FPS)

        if not video_stream.isOpened():  # 检查视频流是否成功打开
            print("错误: 无法打开视频流。")
        while True:  # 持续读取视频帧
            start_time = time.time()  # 记录帧处理开始时间
            ret, frame = video_stream.read()  # 读取视频帧
            if not ret:  # 如果未成功读取帧
                print("错误: 无法读取帧")
                break  # 退出循环
            #logger.info(f"cam: {w} x {h} @ {fps}") 
            info = detector.detect_armor(frame)  # 使用 detector 进行检测
<<<<<<< HEAD
            # bin, img = detector.display()
            # cv2.imshow("bin",bin)
            # cv2.imshow("img",img)
=======
            bin, img = detector.display()
            cv2.imshow("bin",bin)
            cv2.imshow("img",img)
>>>>>>> ff6d6d34e1c8e125dff207d83b8d7b7810679c45
            target_yaw, target_pitch = tracker.track(info)
            transfer.send(target_yaw, target_pitch)
            end_time = time.time()  # 记录帧处理结束时间
            detection_time = (end_time - start_time) * 1000  # 转换为毫秒
            #logger.debug(f"检测延迟: {int(detection_time)} 毫秒")  # 输出检测延迟
            if cv2.waitKey(1) & 0xFF == ord("q"):  # 检测按键
                break  # 退出循环
        video_stream.release()  # 释放视频流
        cv2.destroyAllWindows()  # 关闭所有窗口
        transfer.close()
        logger.info("off")
    
detect_color =  0  # 颜色参数 0: 识别红色装甲板, 1: 识别蓝色装甲板, 2: 识别全部装甲板
# 图像参数字典
<<<<<<< HEAD
binary_val = 80    
=======
binary_val = 63  
>>>>>>> ff6d6d34e1c8e125dff207d83b8d7b7810679c45
light_params = {
    "light_area_min": 15,  # 最小灯条面积
    "light_angle_min": -45,  # 最小灯条角度
    "light_angle_max": 45,  # 最大灯条角度
    "light_angle_tol": 10,  # 灯条角度容差
    "vertical_discretization": 0.615,  # 垂直离散
    "height_tol": 18,  # 高度容差
    "cy_tol":11,  # 中心点的y轴容差
    "height_multiplier": 3.5
}
# 颜色参数字典
color_params = {
    "armor_color": {1: (255, 255, 0), 0: (128, 0, 128)},  # 装甲板颜色映射
    "armor_id": {1: 1, 0: 7},  # 装甲板 ID 映射
    "light_color": {1: (200, 71, 90), 0: (0, 100, 255)},  # 灯条颜色映射
    "light_dot": {1: (0, 0, 255), 0: (255, 0, 0)}  # 灯条中心点颜色映射
}
cam_params = { 
        "width": 640,  # 你想要的宽度
        "height": 480,   # 你想要的高度
        "fps": 180,  # 你想要的帧率
        "cam_num": 4  # 摄像头编号
}
# 配置串口参数
serial_port = '/dev/ttyS2'  # 根据实际情况修改
baud_rate = 115200       # 波特率
timeout = 1            # 超时设置
detector = ArmorDetector(detect_color, 2, binary_val, light_params, color_params)  # 创建检测器对象
tracker = ArmorTracker(detect_color)
<<<<<<< HEAD
tracker.frame_add = 0
tracker.vfov = 36
=======
tracker.frame_add = 3
tracker.vfov = 72
>>>>>>> ff6d6d34e1c8e125dff207d83b8d7b7810679c45
transfer = Trans(serial_port, baud_rate, timeout)
cam = Cam(cam_params)
cam.detect(detector, tracker, transfer)

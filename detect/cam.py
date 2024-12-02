import cv2  # 导入 OpenCV 库
import time  # 导入时间库
from detector import ArmorDetector  # 从 detector 导入 Detector 类
from adjust import Adjust  # 导入调试代码
from loguru import logger

class Cam():
    def __init__(self, run_mode, cam_params):
        self.mode = run_mode["mode"]
        self.video = run_mode["video"]
        self.url = run_mode["url"]
        self.image_path = run_mode["image_path"]     
        self.width = cam_params["width"]  # 你想要的宽度
        self.height = cam_params["height"]   # 你想要的高度
        self.fps = cam_params["fps"]  # 你想要的帧率
        self.cam_num = cam_params["cam_num"]
        self.exposure = cam_params["exposure_value"]

    def run(self, detector, adjust):
        if self.mode in [0, 2]:  # 处理视频流
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
            video_stream.set(cv2.CAP_PROP_EXPOSURE, self.exposure)
            if not video_stream.isOpened():  # 检查视频流是否成功打开
                print("错误: 无法打开视频流。")
            if self.mode == 0:
                adjust.setup_windows()  # 创建滑动条窗口
            while True:  # 持续读取视频帧
                start_time = time.time()  # 记录帧处理开始时间
                ret, frame = video_stream.read()  # 读取视频帧
                if not ret:  # 如果未成功读取帧
                    print("错误: 无法读取帧")
                    break  # 退出循环
                
                info = detector.detect_armor(frame)  # 使用 detector 进行检测
                if adjust.flag:
                    detector.binary_val = adjust.binary_val
                    detector.light_params = adjust.light_params
                    adjust.flag = False
                if self.mode == 0:
                    binary, result = detector.display()
                    cv2.imshow("result", result)
                    cv2.imshow("binary", binary)
                
                end_time = time.time()  # 记录帧处理结束时间
                detection_time = (end_time - start_time) * 1000  # 转换为毫秒
                logger.info(f"class_id: {info}")  # 输出检测结果
                logger.debug(f"检测延迟: {int(detection_time)} 毫秒")  # 输出检测延迟
                logger.info(f"cam: {w} x {h} @ {fps}")  # 输出检测结果
                if cv2.waitKey(1) & 0xFF == ord("q"):  # 检测按键
                    break  # 退出循环
            video_stream.release()  # 释放视频流
            cv2.destroyAllWindows()  # 关闭所有窗口

        elif self.mode == 1:  # 实时处理静态图像
            current_frame = cv2.imread(self.image_path)  # 读取静态图像
            if current_frame is None:  # 检查图像是否读取成功
                print("错误: 无法读取图像。请检查路径:", self.image_path)  # 输出错误信息
            adjust.setup_windows()  # 创建滑动条窗口
            while True:  # 持续处理图像
                start_time = time.time()  # 记录帧处理开始时间
                info = detector.detect_armor(current_frame)  # 使用 detector 进行检测
                detector.display()
                if adjust.flag:
                    detector.binary_val = adjust.binary_val
                    detector.light_params = adjust.light_params
                    adjust.flag = False
                end_time = time.time()  # 记录帧处理结束时间
                detection_time = (end_time - start_time) * 1000  # 转换为毫秒
                logger.info(f"class_id: {info}")  # 输出检测结果
                logger.debug(f"检测延迟: {int(detection_time)} 毫秒")  # 输出检测延迟
                if cv2.waitKey(1) & 0xFF == ord("q"):  # 检测按键
                    break  # 退出循环
            cv2.destroyAllWindows()  # 关闭所有窗口

        else:  # 如果模式无效
            print("无效的模式，程序结束。")  # 输出错误信息
            
if __name__ == "__main__":
    # 模式参数字典
    detect_color =  0  # 颜色参数 0: 识别红色装甲板, 1: 识别蓝色装甲板, 2: 识别全部装甲板
    display_mode = 2 # 显示模式 0: 不显示, 1: 显示二值化图, 2: 显示二值化图和结果图像
    # 图像参数字典
    binary_val = 78  
    light_params = {
        "light_area_min": 19,  # 最小灯条面积
        "light_angle_min": -45,  # 最小灯条角度
        "light_angle_max": 45,  # 最大灯条角度
        "light_angle_tol": 20,  # 灯条角度容差
        "vertical_discretization": 615,  # 垂直离散
        "height_tol": 34,  # 高度容差
        "cy_tol":24,  # 中心点的y轴容差
        "height_multiplier": 25 
    }
    # 颜色参数字典
    color_params = {
        "armor_color": {1: (255, 255, 0), 0: (128, 0, 128)},  # 装甲板颜色映射
        "armor_id": {1: 1, 0: 7},  # 装甲板 ID 映射
        "light_color": {1: (200, 71, 90), 0: (0, 100, 255)},  # 灯条颜色映射
        "light_dot": {1: (0, 0, 255), 0: (255, 0, 0)}  # 灯条中心点颜色映射
    }
    run_mode = {
        "mode": 0,  # 模式设置 0: 视频流, 1: 静态图, 2: 无调试
        "video": False,  # 是否使用视频
        "url": "./photo/test.mp4",  # 视频路径
        "image_path": "./photo/red_1.jpg"  # 图片路径
    }
    cam_params = { 
            "width": 640,  # 你想要的宽度
            "height": 480,   # 你想要的高度
            "fps": 180, # 你想要的帧率
            "cam_num": 4,  # 摄像头编号"
            "exposure_value": 0 # 曝光值
    }
    detector = ArmorDetector(detect_color, display_mode, binary_val, light_params, color_params)  # 创建检测器对象
    adjust = Adjust(light_params, binary_val)
    cam = Cam(run_mode, cam_params)
    cam.run(detector, adjust)
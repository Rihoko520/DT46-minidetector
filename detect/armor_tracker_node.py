import time                             # JSON序列化库
from armor_tracker import select_tracking_armor , pixel_to_angle_and_deep
from Kalman import KalmanFilter
from loguru import logger
import time  # 导入时间模块


def time_diff(last_time=[None]):
    """计算两次调用之间的时间差，单位为纳秒。"""
    current_time = time.time_ns()  # 获取当前时间（单位：纳秒）

    if last_time[0] is None:  # 如果是第一次调用，更新last_time
        last_time[0] = current_time
        return 0.1  # 防止除零错误，返回1纳秒

    else:  # 计算时间差
        diff = current_time - last_time[0]  # 计算时间差（单位：纳秒）
        last_time[0] = current_time  # 更新上次调用时间
        return diff / 1e9  # 返回时间差（秒）
    
class ArmorTracker():
    def __init__(self, color):
        self.pic_width = 640       # 随便初始化一个图像宽度
        self.center_last = (0, 0)   # 默认初始化中心点坐标为(0, 0)
        self.height_last = 0             # 初始化armmor高度为0
        self.use_kf = True          # 是否使用卡尔曼滤波
        self.kf_cx = KalmanFilter()
        self.kf_cy = KalmanFilter()
        self.height = 0
        self.lost = 0               # 初始化丢失帧数
        self.frame_add = 0         # 初始化补帧数
        self.tracking_color = color    # 1蓝色表示, 0表示红色, 现初始化为红色
        self.vfov = 45

    def track(self, info):
        tracking_armor = select_tracking_armor(info, self.tracking_color)  # 0表示红色
        if not tracking_armor :  # 检查 tracking_armor 是否为空
            if self.use_kf == True :
                self.lost += 1
                if self.lost <= self.frame_add:
                    self.kf_cx.predict()  # 进行预测
                    self.kf_cy.predict()
                    self.center_last = (self.kf_cx.get_state(), self.kf_cy.get_state())  # 获取预测的状态
                    logger.info(f"预测的 cx: {self.center_last[0]}, cy: {self.center_last[1]}, h: {self.height}")
                else :
                    self.center_last = (0, 0) 
            else :
                self.center_last = (0, 0)

        else :
            # if "center" in tracking_armor and "height" in tracking_armor:
            self.center_last = tracking_armor["center"]
            if self.use_kf == True :
                self.lost = 0
                self.kf_cx.predict()  # 进行预测
                self.kf_cy.predict()
                self.kf_cx.update(self.center_last[0])  # 更新状态   
                self.kf_cy.update(self.center_last[1])  # 更新状态        
                self.center_last = (self.kf_cx.get_state(), self.kf_cy.get_state())  # 获取预测的状态
                self.height = tracking_armor["height"]
                logger.info(f"预测的 cx: {self.center_last[0]}, cy: {self.center_last[1]}, h: {self.height}")
        yaw, pitch = pixel_to_angle_and_deep(self.center_last, self.vfov, self.pic_width) 
        logger.info(f'发送 yaw: {yaw}, pitch: {pitch}')
        return yaw, pitch


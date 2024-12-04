# PID 控制器类
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp  # 比例系数
        self.Ki = Ki  # 积分系数
        self.Kd = Kd  # 微分系数
        self.previous_error = 0  # 上一次误差
        self.integral = 0  # 积分值

    def update(self, setpoint, measured_value): # 更新PID参数 setpoint 为目标角度，measured_value 为当前角度
        error = setpoint - measured_value  # 计算误差
        self.integral += error  # 积分
        derivative = error - self.previous_error  # 计算微分

        # PID 输出
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = error  # 更新上一次误差

        return output  # 返回控制输出


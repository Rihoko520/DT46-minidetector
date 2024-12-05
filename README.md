# gimbal-esp
coded by retard
# 创建开机自启服务（非必须步骤）


## 新建文件:
```bash
sudo nano /etc/systemd/system/rcv.service 
```

## cv.service
```bash
[Unit]
Description = rcv Prediction Node
After = network.target

[Service]
Type = simple

User = pi
Group = pi

ExecStartPre= /bin/sleep 5
ExecStart = /home/pi/DT46-minidetector/start.sh
ExecStop = /home/pi/DT46-minidetector/stop.sh
Restart = always
TimeoutStopSec = 30
RestartSec = 10s

[Install]
WantedBy = multi-user.target
```

## 启用服务
```bash
sudo systemctl daemon-reload
sudo systemctl start rcv.service
sudo systemctl status rcv.service
sudo systemctl enable rcv.service

```

## stop
```bash
sudo systemctl stop rcv.service
```

## start.sh
### 3. 使用 `sudo` 结合 NOPASSWD

如果你希望普通用户能够在不输入密码的情况下运行某个特定命令，可以通过 `sudoers` 文件进行配置：

1. 运行 `visudo` 命令编辑 `sudoers` 文件：

   ```bash
   sudo visudo
   ```

2. 在文件末尾添加以下内容，将 `username` 替换为普通用户的用户名：

   ```plaintext
   username ALL=(ALL) NOPASSWD: /path/to/python3 /home/pi/DT46-minidetector/detect/main.py
   ```

这样，用户可以通过以下命令运行该脚本**(start.sh)**而无需输入密码：

```bash
sudo /path/to/python3 /home/pi/DT46-minidetector/detect/main.py
```

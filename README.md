# gimbal-esp
coding for retard
## 创建开机自启服务（非必须步骤）



新建文件:
```bash
sudo nano /etc/systemd/system/cv.service 
```
cv.service
```service
[Unit]
Description=cv Prediction Node
After=network.target

[Service]
Type=simple

User=pi
Group=pi

ExecStartPre=/bin/sleep 5
ExecStart=/home/rihoko/detector-mini/start.sh
ExecStop=/home/rihoko/detector-mini/stop.sh
Restart=always
TimeoutStopSec=30
RestartSec=10s

[Install]
WantedBy=multi-user.target
```
启用服务
```bash
sudo systemctl daemon-reload
sudo systemctl start cv.service
sudo systemctl status cv.service

sudo systemctl enable cv.service
```

stop
```bash
journalctl -u cv.service

sudo systemctl stop cv.service
```
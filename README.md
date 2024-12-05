# gimbal-esp
coding for retard
## 创建开机自启服务（非必须步骤）


新建文件:
```bash
sudo nano /lib/systemd/system/cv.service
```

cv.service
```service
[Unit]
Description=Expand partition size

[Service]
Type = oneshot
ExecStart =python /home/pi/DT46-minidetector/detect/main.py
RemainAfterExit = yes
StandardOutput = null

[Install]
WantedBy = multi-user.target
```

保存后给该文件最高权限：
```
sudo chmod 777 /lib/systemd/system/cv.service
```

启用服务
```bash
sudo systemctl enable cv.service
```

stop
```bash
journalctl -u cv.service
sudo systemctl stop cv.service
```
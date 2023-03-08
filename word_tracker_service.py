import os


def register_as_service():
    """注册为 Systemd 服务"""
    os.system(
        "sudo ln ~/scripts/word-tracker.service /etc/systemd/system/word-tracker.service"
    )
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl enable word-tracker.service")
    os.system("sudo systemctl start word-tracker.service")


# 注册为系统服务
register_as_service()

import os
from celery import Celery

# 设置默认的Django设置模块，确保你的项目的settings.py位于backend_app包内
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('backend_app', broker='redis://0.0.0.0:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()

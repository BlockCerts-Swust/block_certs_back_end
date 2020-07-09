import os
from celery import Celery
import time


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'block_certs_back_end.settings')

app = Celery('block_certs_back_end')
app.config_from_object('django.conf:settings', namespace='block_certs_back_end')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    time.sleep(5)
    print("Weeeee")
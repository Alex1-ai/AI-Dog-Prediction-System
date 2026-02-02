# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 1
worker_class = "sync"
threads = 1
timeout = 300
preload_app = True

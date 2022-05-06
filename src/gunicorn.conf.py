bind = '0.0.0.0:10000'
accesslog = '-'
access_log_format = '%(h)s %(u)s "%(r)s" %(s)s "%(f)s" "%(a)s"'
errorlog = '-'
loglevel = 'info'
workers = 1
wsgi_app = 'app:app'
from environ import FileAwareEnv
from dotenv import load_dotenv, find_dotenv
from multiprocessing import cpu_count
from pathlib import Path

env = FileAwareEnv()
load_dotenv(find_dotenv())

bind = '0.0.0.0:80'
workers = min(cpu_count(), 3) # don't hog system resources
max_requests = 10
max_requests_jitter = 5

# accesslog = '-' # skip access log (can get from nginx)
errorlog = '-'
loglevel = 'info' if env.bool('DEBUG', default=False) else 'error'
capture_output = True
control_socket_disable = True

# handle dev reloading
reload = env.bool('GUNICORN_RELOAD', default=False)
# handle extra files for reload
def getDirExtraFiles(dir):
    return [
        str(path) for path in list((dir / 'static/').rglob('*.*')) + list((dir / 'templates/').rglob('*.*'))
    ]
BASE_DIR = Path(__file__).parent
reload_extra_files = getDirExtraFiles(BASE_DIR / 'digital_mary/') + \
    getDirExtraFiles(BASE_DIR / 'digital_mary_app/') + \
    getDirExtraFiles(BASE_DIR / 'digital_mary_challenges/') + \
    getDirExtraFiles(BASE_DIR / 'digital_mary_config/') \
    if reload else []
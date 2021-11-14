__all__ = [
    'API_TOKEN',
    'WEBHOOK_HOST',
    'WEBHOOK_PORT',
    'WEBHOOK_LISTEN',
    'WEBHOOK_URL_BASE',
    'WEBHOOK_URL_PATH'
]

import os

WEBHOOK_PORT = int(os.environ.get('PORT', 5000)) # 
API_TOKEN =  os.environ.get('TYS_BOT_TOKEN')

WEBHOOK_HOST = 'takeyourseats.herokuapp.com' # this is the name of heriku aap
WEBHOOK_LISTEN = '0.0.0.0'  

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"


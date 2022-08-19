import os
from config.utils import get_config_value, PACKAGE_PATH


LOG_LEVEL = "DEBUG"

LOG_DIR = get_config_value("LOG_PATH")
LOG_DIR = LOG_DIR if LOG_DIR else "logs"
LOG_PATH = os.path.join(PACKAGE_PATH, LOG_DIR)
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

    
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
        'standard': {
            'format': '[%(asctime)s][%(levelname)s][%(name)s:%(lineno)s]%(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
    },
    'handlers': {
        "app_logfile": {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'aplyproject_app.log'),
            'when': 'D',    # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 30,  # how many backup file to keep, 10 days
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        'api_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'ablyproject_api.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        'err_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'ablyproject_err.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        'db_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'dazoom_db.log'),
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 30,  # how many backup file to keep, 10 days
            'formatter': 'standard'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['app_logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['db_logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        "api": {
            'handlers': ['api_logfile'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        "err": {
            "handlers": ["err_logfile"],
            "level": LOG_LEVEL,
            "propagate": False
        }
    }
}

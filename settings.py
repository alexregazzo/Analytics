import os
import logging.config


def logmaker(name: str):
    return logging.getLogger(f"WebTracker.{name}")


DEVELOMENT_MODE = True
LOG_FORMAT = "%(asctime)s - %(levelname)s :: %(name)s %(lineno)d :: %(message)s"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ROOT_DIRPATH = os.path.join(os.path.dirname(__file__))
LOG_DIRPATH = os.path.join(ROOT_DIRPATH, 'log')
os.makedirs(LOG_DIRPATH, exist_ok=True)

# Setup log
LOG_CONFIG_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIRPATH, 'debug.log'),
            'mode': 'w' if DEVELOMENT_MODE else 'a'
        },
        'stream':
            {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            }
    },
    'loggers': {
        'WebTracker': {
            'handlers': ['default'],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(LOG_CONFIG_DICT)
logger = logging.getLogger("WebTracker")

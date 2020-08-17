import os
import sys
import logging
import datetime
from datetime import timedelta
import time
from autofix.util.Config import Config
from autofix.util.FileSystemUtil import expandPath
from autofix.util.Singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        self.dockerBuildIdx = ''
        self.dockerLogger = None
        self.schemeLogger = None
        self.targetLogger = None

    @property
    def logDir(self) -> str:
        return os.path.join(expandPath(Config().get('PATH', 'LOG_DIR_PATH')), self.dockerBuildIdx)


def TW_Time(sec, what):
    taipei_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return taipei_time.timetuple()


def _configLogger(name: str, level=logging.DEBUG, file=True) -> logging.Logger:
    """Return logging.Logger

    :param name: name of the logger
    :param level: logging level of the logger
    :param file: whether write log to a log file
    :return: the configured logger
    """
    if file:
        base = Logger().logDir
        if len(base) == 0 or not os.path.exists(base) or not os.path.isdir(base):
            base = os.path.abspath('.')
        path = os.path.join(base, '{}.log'.format(name))
        handler = logging.FileHandler(path, 'a', 'utf-8', False)
    else:
        handler = logging.StreamHandler(sys.stdout)
    logging.Formatter.converter = TW_Time
    handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)-5s] %(message)s', '%Y-%m-%d %H:%M:%S'))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def _addLoggingLevel(level: str, prior: int):
    level = level.upper()
    method = level.lower()

    if hasattr(logging, level) or hasattr(logging, method) or hasattr(logging.getLoggerClass(), method):
        return

    def logToRoot(message, *args, **kwargs):
        logging.log(prior, message, *args, **kwargs)

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(prior):
            self._log(prior, message, args, **kwargs)

    logging.addLevelName(prior, level)
    setattr(logging, level, prior)
    setattr(logging, method, logToRoot)
    setattr(logging.getLoggerClass(), method, logForLevel)


def dockerModeLogger(index: str):
    _addLoggingLevel('STAGE', int((logging.INFO + logging.WARNING) / 2))
    _addLoggingLevel('START', int((logging.INFO + logging.WARNING) / 2 + 1))
    _addLoggingLevel('FINAL', int((logging.INFO + logging.WARNING) / 2 - 1))
    Logger().dockerBuildIdx = index
    Logger().dockerLogger = _configLogger(index)
    Logger().schemeLogger = _configLogger('scheme', logging.INFO, False)


def normalModeLogger():
    Logger().schemeLogger = _configLogger(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), logging.INFO, True)


def newTargetLogger(index: str):
    if Logger().dockerLogger is not None:
        Logger().targetLogger = Logger().dockerLogger
    else:
        Logger().targetLogger = _configLogger('{}-{}'.format(Logger().schemeLogger.name, index))


if __name__ == '__main__':
    exit()

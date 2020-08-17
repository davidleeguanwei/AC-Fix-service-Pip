import configparser
from autofix.util.Singleton import Singleton


class Config(metaclass=Singleton):
    """
    A singleton class for reading configuration file
    Usage example:
        value = Config().get(section, key)
    """

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read('config.ini', 'utf-8')

    def get(self, section: str, key: str) -> str:
        if section.upper() not in self._config.keys():
            return ''
        elif key.upper() not in self._config[section.upper()].keys():
            return ''
        return self._config[section.upper()][key.upper()]


if __name__ == '__main__':
    exit()

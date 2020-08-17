import time
import requests
from bs4 import BeautifulSoup
from autofix.util.Config import Config


lastQueryTime = 0
queryInterval = float(Config().get('QUERY', 'INTERVAL'))


def getURLSoup(url: str) -> BeautifulSoup:
    """Return a BeautifulSoup object

    :param url: the query URL
    :return: the parsed content in BeautifulSoup if receive 200, else an empty BeautifulSoup
    """
    global lastQueryTime, queryInterval
    while time.time() < lastQueryTime + queryInterval:
        time.sleep(1)
    lastQueryTime = time.time()
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    if response.status_code != 200:
        return BeautifulSoup('', 'lxml')
    return BeautifulSoup(response.text, 'lxml')


def headURL(url: str) -> bool:
    """Return a boolean

    :param url: the target url
    :return: whether the url can be reached (respond HEAD request in 10 seconds)
    """
    try:
        response = requests.head(url, timeout=10)
    except requests.exceptions.RequestException:
        return False
    if response.status_code == 200:
        return True
    elif response.status_code == 301:
        return headURL(response.headers['Location'])
    elif response.status_code == 302:
        return headURL(response.headers['Location'])


if __name__ == '__main__':
    exit()

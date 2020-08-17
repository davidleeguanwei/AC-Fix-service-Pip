import json
import time
import requests
import sys
from bs4 import BeautifulSoup

def retriveDownloadFileFromPyPI(param):
	param = param.split("==")
	if len(param) == 2:
		req = requests.get("https://pypi.org/project/"+param[0]+"/"+param[1]+"/#files")
	else:
		req = requests.get("https://pypi.org/project/"+param[0]+"/#files")

	if req.status_code == requests.codes.ok:
		soup = BeautifulSoup(req.text, 'html.parser')
		results = soup.find_all('div', {'class' : 'vertical-tabs__content'})
	else:
		results = False

	if not results:
		print("Request error with code " + str(req.status_code))
	elif results == None:
		print("No git repo")
	else:
		links = []
		for r in results:
			h2_child = r.find('h2')
			if h2_child.text == "Download files":
				children = r.find('table', {'class': 'table table--downloads'})
				children = children.find_all('th', {'scope': 'row'})
				for child in children:
					child = child.find('a')['href']
					links.append(child)
				return links

	return None

if __name__ == "__main__":
		exit()

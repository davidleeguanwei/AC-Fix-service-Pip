import json
import time
import requests
import sys
from bs4 import BeautifulSoup

def retriveGitRepoFromPyPI(repo):
	param = repo
	req = requests.get("https://pypi.org/project/" + param)

	if req.status_code == requests.codes.ok:
		soup = BeautifulSoup(req.text, 'html.parser')
		results = soup.find_all('div', {'class' : 'sidebar-section'})
	else:
		results = False

	if not results:
		print("Request error with code " + str(req.status_code))
	elif results == None:
		print("No git repo")
	else:
		git_repo = []
		for r in results:
			h3_child = r.find('h3')
			if h3_child.text == "Project links":
				children = r.find_all('a', {'class': 'vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed'})
				for child in children:
					git_repo.append(child['href'])
				return git_repo

	return None

if __name__ == "__main__":
        exit()

from autofix.util.RequestUtil import getURLSoup, headURL


def queryRepo(repo: str) -> str:
    """Return a string

    Query API: https://mvnrepository.com/repos/[REPO_KEY]

    Crawling steps:
    1. Query HTML content
    2. Retrieve rows in the 1st table of division with id='maincontent'
    3. Return the 'td' cell content in the row of 'URL'

    :param repo: query name of the target repository
    :return: the URL of the target repository, an empty string if not exists
    """
    soup = getURLSoup('https://mvnrepository.com/repos/{}'.format(repo))

    try:
        table = soup.find(id='maincontent').find_all('table', attrs={'class': 'grid'})[0]
        rows = table.find_all('tr')
    except (AttributeError, IndexError):
        return ''

    for row in rows:
        if row.find('th') is None or row.find('th').text != 'URL':
            continue
        if row.find('td') is not None:
            return row.find('td').text

    return ''


def queryArtifactRepo(group: str, name: str, version: str) -> list:
    """Return a list

    Query API: https://mvnrepository.com/artifact/[GROUP]/[NAME]/[VERSION]

    Crawling steps:
    1. Query HTML content
    2. Retrieve rows in the 1st table of division with id='maincontent'
    3. Retrieve 'a' tags from the 'td' cell in the row of 'Repositories', and query repository URLs with the links

    :param group: the group of the target artifact
    :param name: the name of the target artifact
    :param version: the version of the target artifact
    :return: the repository URLs containing the target artifact
    """
    repos = list()
    repositories = list()
    extensions = list()
    soup = getURLSoup('https://mvnrepository.com/artifact/{}/{}/{}'.format(group, name, version))

    try:
        table = soup.find(id='maincontent').find_all('table', attrs={'class': 'grid'})[0]
        rows = table.find_all('tr')
    except (AttributeError, IndexError):
        return repos

    for row in rows:
        if row.find('th') is None or row.find('td') is None:
            continue
        if row.find('th').text == 'Repositories':
            repositories = [queryRepo(a.get('href').split('/')[-1]) for a in row.find('td').find_all('a')]
        elif row.find('th').text == 'Files':
            extensions = [a.get('href').split('.')[-1] for a in row.find('td').find_all('a') if a.text != 'View All']
    if len(extensions) == 0:
        extensions.append('jar')

    for repository in repositories:
        available = True
        for extension in extensions:
            artifact_url = '{}/{}/{}/{}-{}.{}'.format(group.replace('.', '/'), name, version, name, version, extension)
            if not headURL(repository + ('' if repository[-1] == '/' else '/') + artifact_url):
                available = False
        if available:
            repos.append(repository)

    return repos


def queryArtifactVersion(group: str, name: str) -> list:
    """Return a list

    Query API: https://mvnrepository.com/artifact/[GROUP]/[NAME](Optional: ?repo=[REPO_NAME])

    Crawling steps:
    1. Query HTML content
    2. Retrieve tabs from the unordered list of division with id='snippets'
    3. Retrieve query link from each tab
    4. Retrieve all 'vbtn' link containing version numbers

    :param group: the group of the target artifact
    :param name: the name of the target artifact
    :return: a list of available versions of the target artifact
    """
    version_list = list()
    soup = getURLSoup('https://mvnrepository.com/artifact/{}/{}'.format(group, name))

    try:
        tabs = soup.find(id='snippets').find('ul', attrs={'class': 'tabs'}).find_all('li')
    except AttributeError:
        return version_list

    queries = list()
    for tab in tabs:
        if tab.find('a') is None:
            continue
        link = tab.find('a').get('href')
        if link is None:
            continue
        queries.append(link.split(name)[-1])

    for query in queries:
        soup = getURLSoup('https://mvnrepository.com/artifact/{}/{}{}'.format(group, name, query))
        try:
            vers = soup.find(id='snippets').find_all('a', attrs={'class': 'vbtn'})
        except AttributeError:
            continue
        for ver in vers:
            link = ver.get('href')
            if link is None:
                continue
            version_list.append(link.split('/')[-1])

    return list(set(version_list))


if __name__ == '__main__':
    exit()

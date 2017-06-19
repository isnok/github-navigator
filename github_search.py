#!/usr/bin/env python
""" Quick Implementation of github search api client.
    Uses the V3 API, described here:

    https://developer.github.com/v3/
    https://developer.github.com/v3/search/
"""

import requests

headers_for_github = requests.utils.default_headers()
headers_for_github.update({
    'User-Agent': 'Github Navigator Assignment Task v0.1',
    'Accept': 'application/vnd.github.v3+json',
    'Time-Zone': 'Europe/Berlin',
})

SEARCH_ENDPOINT = 'http://api.github.com/search/repositories'

def make_session():
    session = requests.Session()
    session.headers.update(headers_for_github)
    return session

def search_repositories(term, session=requests):
    """ Run a search on github, and return the parsed JSON respose.
        The response is wrapped in a dict, to account for possible failures
        of the github api or the network.
    """

    response = session.get(
        SEARCH_ENDPOINT,
        headers=headers_for_github,
        params=[
            ('q', term),
            # ('sort', 'updated'), # we implement our own sorting
            # ('sort', 'stars'),
            # ('sort', 'forks'),
            # ('order', 'desc'),
            # ('order', 'asc'),
        ]
    )
    if response.status_code == 200:
        github_data = response.json()
    else:
        github_data = None
    return {
        'github_status': response.status_code,
        'github_data': github_data,
    }


def repository_details(repo_data, session=requests):
    url = repo_data['commits_url'].replace('{/sha}', '')
    response = session.get(url)
    repo_data = response.json()
    return {
        'github_status': response.status_code,
        'github_data': repo_data,
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        search_term = sys.argv[1]
    else:
        search_term = 'token'

    print("Debug run: {term}".format(term=search_term))

    import pprint

    repos = search_repositories(search_term)
    # pprint.pprint(repos)

    one_repo = repos['github_data']['items'][0]
    pprint.pprint(one_repo)

    pprint.pprint(repository_details(one_repo))

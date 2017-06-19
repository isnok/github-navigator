#!/usr/bin/env python

import dateutil.parser
import logging
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from github_search import make_session, search_repositories, repository_details

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


class NavigatorConfig(object):

    APP_NAME = "Github Navigator"
    DEBUG = True
    SERVER_NAME = 'localhost:9876'
    LOGGER_NAME = 'navigator_app'


app = Flask(__name__)
app.config.from_object('application.NavigatorConfig')

api = Api(app)

def sort_repos(items, **kwargs):

    if 'key' not in kwargs:
        def sort_key__created_at__iso8601(item):
            return dateutil.parser.parse(item['created_at'])
        kwargs['key'] = sort_key__created_at__iso8601

    # default to descending sort
    if 'reverse' not in kwargs:
        kwargs['reverse'] = True

    return sorted(items, **kwargs)

    # alternate version using datetime.strptime:
    # sort_key = lambda item: datetime.datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    # return sorted(items, key=sort_key)

def sort_commits(items, **kwargs):
    """ just to make sure """
    def sort_key__commiter_date__iso8601(item):
        return dateutil.parser.parse(item['commit']['committer']['date'])
    return sorted(items, key=sort_key__commiter_date__iso8601, reverse=True)

term_parser = reqparse.RequestParser()
term_parser.add_argument('search_term', type=str, default='')

class NavigatorSearchResource(Resource):

    def get(self):
        search_term = term_parser.parse_args()['search_term']
        search_result = search_repositories(search_term)
        if search_result['github_status'] == 200:
            return sort_repos(search_result['github_data']['items'])
        else:
            return None

api.add_resource(NavigatorSearchResource, '/api/navigator')


MAX_RESULTS = 5

@app.route('/navigator')
def search_repos():
    search_term = term_parser.parse_args()['search_term']

    session = make_session()
    search_result = search_repositories(
        search_term,
        session=session,
        oauth=OAUTH_CREDENTIALS,
    )

    if search_result['github_status'] == 200:
        repos = sort_repos(search_result['github_data']['items'])
    else:
        repos = []

    repos = repos[:MAX_RESULTS]

    commit_data = {}
    extra_data = {}
    for search_result in repos:
        repo_extra = {
            'datetime_created': dateutil.parser.parse(search_result['created_at']),
        }
        result = repository_details(
            search_result,
            session=session,
            oauth=OAUTH_CREDENTIALS,
        )
        if result['github_status'] == 200:
            commit_data[search_result['id']] = sort_commits(result['github_data'])
            latest_commit_url = result['github_data'][0]['html_url']
            repo_extra['latest_commit_url'] = latest_commit_url
        else:
            commit_data[search_result['id']] = None
            fail_data = result['github_data']
            fail_data['check_url'] = search_result['commits_url'].replace('{/sha}', '')
            fail_data.setdefault('message', None)
            repo_extra.update(fail_data)
        extra_data[search_result['id']] = repo_extra

    return render_template(
        'results.html',
        search_term=search_term,
        items=repos,
        commit_data=commit_data,
        extra_data=extra_data,
    )


OAUTH_CREDENTIALS = {}
def load_oauth_file(name):
    global OAUTH_CREDENTIALS
    try:
        with open(name) as fh:
            import json
            oauth_credentials = json.loads(fh.read())
            assert(isinstance(oauth_credentials['client_id'], basestring))
            assert(isinstance(oauth_credentials['client_secret'], basestring))
            OAUTH_CREDENTIALS = oauth_credentials
            app.logger.info("Successfully loaded OAUTH credentials from '{file}'.".format(file=name))
    except Exception as ex:
        app.logger.info("Failed to load OAUTH credentials from '{file}'.\nException was: {exc}".format(file=name, exc=ex))

load_oauth_file('oauth.json')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

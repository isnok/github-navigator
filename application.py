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

def sort_data(items, **kwargs):

    if 'key' not in kwargs:
        def sort__created_at__iso8601(item):
            return dateutil.parser.parse(item['created_at'])
        kwargs['key'] = sort__created_at__iso8601

    # default to descending sort
    if 'reverse' not in kwargs:
        kwargs['reverse'] = True

    return sorted(items, **kwargs)

    # alternate version using datetime.strptime:
    # sort_key = lambda item: datetime.datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    # return sorted(items, key=sort_key)

term_parser = reqparse.RequestParser()
term_parser.add_argument('search_term', type=str, default='')

class NavigatorSearchResource(Resource):

    def get(self):
        search_term = term_parser.parse_args()['search_term']
        search_result = search_repositories(search_term)
        if search_result['github_status'] == 200:
            return sort_data(search_result['github_data']['items'])
        else:
            return None

api.add_resource(NavigatorSearchResource, '/api/navigator')


MAX_RESULTS = 5

@app.route('/navigator')
def search_repos():
    search_term = term_parser.parse_args()['search_term']

    session = make_session()
    search_result = search_repositories(search_term, session=session)

    if search_result['github_status'] == 200:
        repos = sort_data(search_result['github_data']['items'])
    else:
        repos = []

    repos = repos[:MAX_RESULTS]

    commit_data = {}
    no_commit_data = {}
    for search_result in repos:
        result = repository_details(search_result, session=session)
        if result['github_status'] == 200:
            commit_data[search_result['id']] = result['github_data']
        else:
            commit_data[search_result['id']] = None
            fail_data = result['github_data']
            fail_data['check_url'] = search_result['commits_url'].replace('{/sha}', '')
            fail_data.setdefault('message', None)
            no_commit_data[search_result['id']] = fail_data

    return render_template(
        'results.html',
        search_term=search_term,
        items=repos,
        commit_data=commit_data,
        no_commit_data=no_commit_data,
    )


if __name__ == '__main__':
    app.run()

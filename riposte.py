"""
riposte.py : turn TODOS into issues
"""

import base64
import os
import re

from flask import Flask, request
from github import Github

app = Flask(__name__)

GIT_CLIENT = Github(os.environ['GH_USER'], os.environ['GH_PASSWORD'])

@app.route('/payload', methods=['POST'])
def payload():
    """
    payload : receive post requests when push events happen
    take those push events and comb through all the code that changed
    look for TODO comments and turn them into github issues
    """
    commit_fields = ['added', 'modified']
    files_to_search = set()
    request_json = request.get_json()
    commits = request_json['commits']
    repo = GIT_CLIENT.get_repo(request_json['repository']['full_name'])
    for commit in commits:
        # for every commit, add filenames for new and changed files
        for field in commit_fields:
            for filename in commit[field]:
                files_to_search.add(filename)
    for filename in files_to_search:
        # get the contents of each file
        # search file for todo comments
        # create issue based on comments
        todo_statement = get_todo_from_file(repo, filename)
        if todo_statement:
            repo.create_issue(todo_statement)
    return 'get your post request'

def get_todo_from_file(repo, filename: str) -> str:
    """
    get_todo_from_file : get contents of file from github
    search contents for a todo statement in a comment
    """
    contents = base64.b64decode(repo.get_contents(filename).content)
    re_result = re.search('# TODO: (.*)', str(contents))
    if re_result:
        return [group[0] for group in re_result.groups()]
    return None

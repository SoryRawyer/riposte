"""
riposte.py : turn TODOS into issues
"""

import base64
import hashlib
import os
import re

from flask import Flask, request
from github import Github, GithubException

app = Flask(__name__)

GIT_CLIENT = Github(os.environ['GH_USER'], os.environ['GH_PASSWORD'])

@app.route('/ping', methods=['GET'])
def ping():
    """
    set up ping route to check if service is alive
    """
    return 'pong'

@app.route('/payload', methods=['POST'])
def payload():
    """
    payload : receive post requests when push events happen
    take those push events and comb through all the code that changed
    look for TODO comments and turn them into github issues
    """
    commit_fields = ['added', 'modified']
    files_to_search = set()
    issue_shas = set()
    request_json = request.get_json()
    commits = request_json['commits']
    repo = GIT_CLIENT.get_repo(request_json['repository']['full_name'])
    try:
        label = repo.get_label('todos')
    except GithubException:
        label = repo.create_label('todos', '006b75')
    for issue in repo.get_issues(labels=[label]):
        issue_shas.add(issue.body)
    for commit in commits:
        # for every commit, add filenames for new and changed files
        for field in commit_fields:
            for filename in commit[field]:
                files_to_search.add(filename)
    for filename in files_to_search:
        # get the contents of each file
        # search file for todo comments
        # create issue based on comments
        todo_statements = get_todo_from_file(repo, filename)
        if todo_statements:
            for statement in todo_statements:
                sha1 = hashlib.sha1()
                sha1.update(statement)
                comment_hash = sha1.hexdigest()
                if comment_hash in issue_shas:
                    continue
                repo.create_issue(statement.decode('utf-8'), body=comment_hash, labels=[label])
    return 'get your post request'

def get_todo_from_file(repo, filename: str) -> list:
    """
    get_todo_from_file : get contents of file from github
    search contents for a todo statement in a comment
    """
    contents = base64.b64decode(repo.get_contents(filename).content)
    return re.findall(b'# TODO: (.*)', contents)

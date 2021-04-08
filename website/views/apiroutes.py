from flask import Blueprint, jsonify, request
from website.views.api.rest import GitHubRepo
import asyncio
from json import loads

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

api = Blueprint('api', __name__)


@api.route('/github', methods=["GET", "POST"])
def github():
    if request.method == 'GET':
        URL = "https://github.com/blacksmithop/ambu"
    else:
        URL = loads(request.data).get("url", None)
        if URL is None:
            return jsonify(
                {
                    "error": "Please pass a URL in your POST request"
                }
            )
    myrepo = GitHubRepo(url=URL, loop=loop)
    
    return jsonify(myrepo.stats())
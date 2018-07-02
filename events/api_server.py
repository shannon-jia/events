#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The Application Interface."""

from sanic import Sanic
from sanic.response import json
from sanic_jwt import exceptions
from sanic_jwt import initialize
from sanic_jwt.decorators import protected
import logging
log = logging.getLogger(__name__)

app = Sanic('Events Api Server V1.0')
app.static('/favicon.ico', './favicon.ico')


class User(object):
    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.user_id

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
        }


users = []

username_table = {u.username: u for u in users}
userid_table = {u.user_id: u for u in users}


async def authenticate(request, *args, **kwargs):
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        raise exceptions.AuthenticationFailed(
            "Incorrect username or password.")

    username_table = {u.username: u for u in users}
    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed(
            "Incorrect username or password.")

    if password != user.password:
        raise exceptions.AuthenticationFailed(
            "Incorrect username or password.")

    return user


@app.route("/")
async def index(request):
    return json({
        'name': 'Events Output Api Server',
        'api_version': 'V1.1.0',
        'api': ['v1/cables'],
        'auth': '/auth',
        'modules version': 'IPP-I'
    })


@app.route("/v1/cables")
@protected()
async def handle_events(request):
    return json(app.site.get_cables())


def start(port,
          site=None,
          username='admin',
          password='admin'):
    app.site = site
    users.append(User(2, username, password))
    initialize(app, authenticate=authenticate)
    return app.create_server(host="0.0.0.0",
                             port=port,
                             access_log=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

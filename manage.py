import json
from flask_script import Manager

from factory import create_app
from db import get_user, create_user, db

app = create_app()
manager = Manager(app)


@manager.shell
def _make_context():
    return dict(app=app, db=db, get_user=get_user, create_user=create_user)


if __name__ == '__main__':
    manager.run()

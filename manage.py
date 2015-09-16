print(__name__, '0')

import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

print(__name__, '1')

from app import app, db
app.config.from_object(os.environ['ENV_SETTINGS'])

print(__name__, '2')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

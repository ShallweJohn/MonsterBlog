from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import db, create_app
from config import DevelopmentConfig
from app import models

app = create_app(DevelopmentConfig)

manager = Manager(app)
Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    manager.run()
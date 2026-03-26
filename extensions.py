import pymysql
from flask import g, current_app
from flask_mail import Mail

mail = Mail()

class MySQL:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    @property
    def connection(self):
        if 'mysql_db' not in g:
            port = int(current_app.config.get('MYSQL_PORT', 3306))
            g.mysql_db = pymysql.connect(
                host=current_app.config.get('MYSQL_HOST', 'localhost'),
                user=current_app.config.get('MYSQL_USER', 'root'),
                password=current_app.config.get('MYSQL_PASSWORD', ''),
                db=current_app.config.get('MYSQL_DB', ''),
                port=port,
                autocommit=True,
                ssl={} # Requires SSL for Aiven DB
            )
        return g.mysql_db

    def teardown(self, exception):
        db = g.pop('mysql_db', None)
        if db is not None:
            db.close()

mysql = MySQL()

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
        import time
        port = int(current_app.config.get('MYSQL_PORT', 3306))
        
        if 'mysql_db' not in g:
            retries = 3
            for attempt in range(retries):
                try:
                    g.mysql_db = pymysql.connect(
                        host=current_app.config.get('MYSQL_HOST', 'localhost'),
                        user=current_app.config.get('MYSQL_USER', 'root'),
                        password=current_app.config.get('MYSQL_PASSWORD', ''),
                        db=current_app.config.get('MYSQL_DB', ''),
                        port=port,
                        autocommit=True,
                        connect_timeout=10,
                        ssl={} # Requires SSL for Aiven DB
                    )
                    break
                except Exception as e:
                    print(f"Database connection attempt {attempt + 1} failed: {e}")
                    if attempt == retries - 1:
                        raise
                    time.sleep(2)
        else:
            try:
                g.mysql_db.ping(reconnect=True)
            except Exception:
                # If ping fails, recreate the connection with retries
                retries = 3
                for attempt in range(retries):
                    try:
                        g.mysql_db = pymysql.connect(
                            host=current_app.config.get('MYSQL_HOST', 'localhost'),
                            user=current_app.config.get('MYSQL_USER', 'root'),
                            password=current_app.config.get('MYSQL_PASSWORD', ''),
                            db=current_app.config.get('MYSQL_DB', ''),
                            port=port,
                            autocommit=True,
                            connect_timeout=10,
                            ssl={}
                        )
                        break
                    except Exception as e:
                        print(f"Database ping/reconnect attempt {attempt + 1} failed: {e}")
                        if attempt == retries - 1:
                            raise
                        time.sleep(2)
        return g.mysql_db

    def teardown(self, exception):
        db = g.pop('mysql_db', None)
        if db is not None:
            db.close()

mysql = MySQL()

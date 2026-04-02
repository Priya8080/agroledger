from flask import Flask, render_template
from config import Config
from extensions import mysql, mail
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(Config)

    mysql.init_app(app)
    mail.init_app(app)

    from routes.auth_routes import auth
    from routes.dashboard_routes import dashboard
    
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)

    @app.route('/')
    def home():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
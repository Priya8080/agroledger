from flask import Flask, render_template
from config import Config
from extensions import mysql

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

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
    app.run(debug=True)
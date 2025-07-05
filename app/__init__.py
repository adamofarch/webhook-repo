from flask import Flask, render_template
from app.webhook.routes import webhook


# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # registering all the blueprints
    app.register_blueprint(webhook)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app



import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required

app = Flask(__name__)
app.config.from_object(os.environ['ENV_SETTINGS'])

db = SQLAlchemy(app)


if __name__ == '__main__':  # to avoid import loops
    # from models import User
    import models
    
    print(__name__, '2')
    
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)

    # Create a user to test with
    @app.before_first_request
    def create_user():
        # db.create_all()
        print(app.login_manager._load_user())
        user_datastore.create_user(name='fart', email='fart@fartfart.fart', password='password')
        db.session.commit()

    # Routes
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('user/login.html')
    
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


# print("1")

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# print("2")

app = Flask(__name__)
app.config.from_object(os.environ['ENV_SETTINGS'])

# print("3")

db = SQLAlchemy(app)

if __name__ == '__main__':  # to avoid import loops
    # from models import User
    import models

    @app.route('/')
    def index():
        return render_template('index.html')
    
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    #app.run()

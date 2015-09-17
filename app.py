
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.security import Security, SQLAlchemyUserDatastore, auth_required, login_required, current_user, logout_user


app = Flask(__name__)
app.config.from_object(os.environ['ENV_SETTINGS'])

db = SQLAlchemy(app)


def get_tumblr_client_info(user):
    if user.tumblr_key and user.tumblr_secret:
        tumblr_info = pytumblr.TumblrRestClient(
            os.environ['CLIENT_KEY'],
            os.environ['SECRET_KEY'],
            user.tumblr_key,
            user.tumblr_secret
        ).info().user
        
        if user != current_user: # remove non-public blogs from data
            tumblr_info.blogs = [blog for blog in tumblr_info.blogs if blog.type == 'public']
        
        return tumblr_info
    else:
        return None


if __name__ == '__main__':  # to avoid import loops
    # from models import User
    import models
    
    # Setup login
    bcrypt = Bcrypt(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)
    
    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
    #{
        if request.method == 'POST':
            try:
                user = models.User.query.filter_by(email=request.form['email']).first()
                # user = models.User.filter(email==request.form['email']).first()
                
                if not user:
                    flash('E-mail address not recognized.', 'error')
                    return redirect(url_for('login'))
                
                if bcrypt.check_password_hash(user.password, request.form['password']):
                    login_user(user)
                    flash('login-success', 'login success')
                    return redirect(url_for('user_dash'))
                else:
                    flash('Password was incorrect.', 'error')
                    return redirect(url_for('login'))
            except NameError:
                flash('There were missing fields in the data you submitted.', 'error')
                return redirect(url_for('login'))
        return render_template('user/login.html')
    #}
    
    # USER SIGN UP
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
    #{
        if request.method == 'POST': # Form data submitted
            try:
                new_user_data = \
                {
                    'name': request.form['name'],
                    'email': request.form['email'],
                    'password': bcrypt.generate_password_hash(request.form['password'])
                }
                
                new_user = models.User(**new_user_data)
                db.session.add(new_user)
                db.session.commit()
                
                flash('Your account has been created and you can now log in.', 'success')
                return redirect(url_for('login'))
            except NameError:
                flash('There were missing fields in the data you submitted.', 'error')
                return redirect(url_for('signup'))
            # except IntegrityError:
            #     flash('That e-mail address or display name is already in use.');
            # not sure it was IntegrityError when uniqueness violated...
            
        else: # GET: Show sign up form
            if not current_user.is_authenticated: # but not if they're already logged in
                return render_template('user/new.html')
            else:
                return redirect(url_for('user_dash'))
    #}
    
    # USER LOG OUT
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    # SHOW USER
    @app.route('/user/<int:id>')
    def user_show(id):
        user = models.User.query.get_or_404(id)#.options(joinedload('works'))
        
        if user == current_user:
            return redirect(url_for('user_dash'))
        
        tumblr_info = get_tumblr_client_info(user)
        return render_template('user/show.html', user=user, tumblr_info=tumblr_info)
    
    # USER DASHBOARD
    @app.route('/user/dash')
    @login_required
    def user_dash():
        tumblr_info = get_tumblr_client_info(current_user)#.options(joinedload('works'))
        return render_template('user/show.html', user=current_user, tumblr_info=tumblr_info)
    

    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


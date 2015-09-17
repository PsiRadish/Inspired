
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

from requests_oauthlib import OAuth1Session
import pytumblr

app = Flask(__name__)
app.config.from_object(os.environ['ENV_SETTINGS'])

db = SQLAlchemy(app)

# app.tumblr_request_url
# app.tumblr_auth_base_url
# app.tumblr_access_token_url
oauth_sessions = {}

if __name__ == '__main__':  # to avoid import loops
#{
    def get_tumblr_info(user):
    #{
        global oauth_sessions
        
        if user.tumblr_key and user.tumblr_secret:
            tumblr_info = pytumblr.TumblrRestClient(
                app.config['TUMBLR_CLIENT'],
                app.config['TUMBLR_SECRET'],
                user.tumblr_key,
                user.tumblr_secret
            ).info()
            
            if not 'user' in tumblr_info: # ouath failed
                tumblr_info['user'] = None
            elif user != current_user: # filter data to only show public blogs
                tumblr_info.user.blogs = [blog for blog in tumblr_info.user.blogs if blog.type == 'public']
            
            return tumblr_info
        elif user == current_user:
            tumblr_oauth = OAuth1Session(app.config['TUMBLR_CLIENT'], client_secret=app.config['TUMBLR_SECRET'], callback_uri=app.config['TUMBLR_CALLBACK_URL'])
            
            fetch_response = tumblr_oauth.fetch_request_token(app.config['TUMBLR_REQUEST_URL'])
            authorization_url = tumblr_oauth.authorization_url(app.config['TUMBLR_AUTH_BASE_URL'])
            
            # store this OAuth1Session to use again in the callback route (which will receive the same oauth_token)
            oauth_sessions[fetch_response['oauth_token']] = tumblr_oauth
            
            return { 'user': None, 'oauth_url': authorization_url }
        else:
            return { 'user': None }
    #}
    
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
                assert len(request.form['password']) >= 8
                
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
            except AssertionError:
                flash('Password not long enough.', 'error')
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
        
        tumblr_info = get_tumblr_info(user)
        return render_template('user/show.html', user=user, tumblr_info=tumblr_info)
    
    # USER DASHBOARD
    @app.route('/user/dash')
    @login_required
    def user_dash():
        tumblr_info = get_tumblr_info(current_user)#.options(joinedload('works'))
        return render_template('user/show.html', user=current_user, tumblr_info=tumblr_info)
    
    # TUMBLR CALLBACK
    @app.route('/user/dash/tumblr')
    @login_required
    def tumblr_callback():
        try:
            # retrieve the OAuth1Session matching this oauth_token
            tumblr_oauth = oauth_sessions[request.args['oauth_token']]
            
            tumblr_oauth.parse_authorization_response(request.url)
            access_tokens = tumblr_oauth.fetch_access_token(app.config['TUMBLR_ACCESS_TOKEN_URL'])
            
            current_user.tumblr_key = access_tokens['oauth_token']
            current_user.tumblr_secret = access_tokens['oauth_token_secret']
            db.session.commit()
            
            flash('Tumblr authorization successful.', 'success')
        except NameError as err:
            print(err)
            flash('Tumblr authorization failed.', 'error')
        
        return redirect(url_for('user_dash'))

    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
#}

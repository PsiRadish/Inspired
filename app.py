
import os
import re
from flask import Flask, Response, render_template, redirect, url_for, request, flash, session
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

from requests_oauthlib import OAuth1Session
import pytumblr

from sanitize import sanitize


app = Flask(__name__)
app.config.from_object(os.environ['ENV_SETTINGS'])

db = SQLAlchemy(app)

# app.tumblr_request_url
# app.tumblr_auth_base_url
# app.tumblr_access_token_url
oauth_sessions = {}

if __name__ == '__main__':  # to avoid import loops
#{
    def create_tumblr_client(user):
        if user.tumblr_key and user.tumblr_secret:
            return pytumblr.TumblrRestClient(
                app.config['TUMBLR_CLIENT'],
                app.config['TUMBLR_SECRET'],
                user.tumblr_key,
                user.tumblr_secret
            )
        return pytumblr.TumblrRestClient(
                app.config['TUMBLR_CLIENT'],
                app.config['TUMBLR_SECRET']) # I think this works?
    
    def get_tumblr_user_info(user, client=None):
    #{
        global oauth_sessions
        
        if client == None:
            client = create_tumblr_client(user)
        
        if user.tumblr_key and user.tumblr_secret:
            tumblr_info = client.info()
            
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
        return models.User.query.options(joinedload('works')).get(user_id)
    
    ####### ROUTES #########
    ########################
    # MAIN INDEX
    @app.route('/')
    def index():
        return render_template('index.html', works=models.Work.query.all())
    
    # LOGIN
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
        elif request.method == 'GET':
            return render_template('user/login.html')
    #}
    
    # NEW USER
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
                    'password': bcrypt.generate_password_hash(request.form['password']),
                    'about': sanitize(request.form.get('about', ""))
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
        elif request.method == 'GET': # Show sign up form
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
        user = models.User.query.options(joinedload('works')).get_or_404(id)
        
        if user == current_user:
            return redirect(url_for('user_dash'))
        
        tumblr_info = get_tumblr_user_info(user)
        return render_template('user/show.html', user=user, tumblr_info=tumblr_info)
    
    # USER DASHBOARD
    @app.route('/user/dash')
    @login_required
    def user_dash():
        tumblr_info = get_tumblr_user_info(current_user)
        return render_template('user/show.html', user=current_user, tumblr_info=tumblr_info)
    
    # TUMBLR CALLBACK
    @app.route('/user/dash/tumblr')
    @login_required
    def tumblr_callback():
        try:
            # retrieve the OAuth1Session matching this oauth_token
            tumblr_oauth = oauth_sessions[request.args['oauth_token']]
            # oauth_sessions[request.args['oauth_token']] = None  # It's been used, remove it from the list
            
            tumblr_oauth.parse_authorization_response(request.url)
            access_tokens = tumblr_oauth.fetch_access_token(app.config['TUMBLR_ACCESS_TOKEN_URL'])
            
            # add_tumblr = \
            # {
            #     'tumblr_key': access_tokens['oauth_token'],
            #     'tumblr_secret': access_tokens['oauth_token_secret']
            # }
            # db.session.query().filter(models.User.id == current_user.id).update(add_tumblr)
            current_user.tumblr_key = access_tokens['oauth_token']
            current_user.tumblr_secret = access_tokens['oauth_token_secret']
            db.session.merge(current_user)
            db.session.commit()
            
            flash('Tumblr authorization successful.', 'success')
        except NameError as err:
            print("NAME_ERROR NAME_ERROR NAME_ERROR", err)
            flash('Tumblr authorization failed.', 'error')
        
        return redirect(url_for('user_dash'))
    
    # NEW WORK
    @app.route('/work/new', methods=['GET', 'POST'])
    @login_required
    def new_work():
    #{
        if request.method == 'POST':
            try:
                new_work_data = \
                {
                    'title': request.form['title'],
                    'fandom_tags': re.split('\s*,\s*', request.form['fandom_tags']),
                    'content_tags': re.split('\s*,\s*', request.form['content_tags']),
                    'char_tags': re.split('\s*,\s*', request.form['char_tags']),
                    'ship_tags': re.split('\s*,\s*', request.form['ship_tags']),
                    'summary': sanitize(request.form['summary'])
                }
                
                new_work = models.Work(**new_work_data)
                new_work.author = current_user
                
                db.session.add(new_work)
                db.session.commit()
                
                flash('New work created.', success)
                return redirect(url_for('add_chapter'))
            except NameError:
                flash('There were missing fields in the data you submitted.', 'error')
                return redirect(url_for('new_work'))
        elif request.method == 'GET':
            return render_template('work/new.html')
    #}
    
    # SHOW_WORK
    @app.route('/work/<work_id>/<chap_order>')
    def show_work(work_id, chap_order):
    #{
        work = models.Work.query.options(joinedload('chapters')).get_or_404(work_id)
        chapter = work.chapters.filter(models.Chapter.order==chap_order).first_or_404()
        
        return render_template('work/show.html', work=work, chapter=chapter)
    #}
    
    # ADD CHAPTER
    @app.route('/work/<work_id>/add', methods=['GET','POST'])
    @login_required
    def add_chapter(work_id):
        if request.method == 'POST':
            try:
                work = models.Work.query.get_or_404(work_id)
                
                new_chapter_data = \
                {
                    'title': request.form['title'],
                    'numeral': request.form['numeral'],
                    'body': sanitize(request.form['body'])
                }
                
                new_chapter = models.Chapter(**new_chapter_data)
                new_chapter.work = work
                
                db.session.add(new_chapter)
                db.session.commit()
                
                flash('Chapter added.', success)
                return redirect(url_for('index'))
            except NameError:
                flash('There were missing fields in the data you submitted.', 'error')
                return redirect(url_for('new_work'))
        
        elif request.method == 'GET':
            work = models.Work.query.options(joinedload('chapters')).get_or_404(work_id)
            default_numeral = "Chapter " + str(len(work.chapters) + 1)
            
            tumblr = current_user.tumblr_key and current_user.tumblr_secret # true or false whether to offer Tumblr import
            
            return render_template('work/add.html', work=work, default_numeral=default_numeral, tumblr=tumblr)
        
    # FRONT-END REQUESTING TUMBLR IMPORT DATA
    @app.route('/api/tumblr-import.json')
    @login_required
    def tumblr_import():
        tumblr_imports = None
        
        if current_user.tumblr_key and current_user.tumblr_secret:
            client = create_tumblr_client(current_user)
            user_info = get_tumblr_user_info(current_user, client)
            
            # collect/trim just the Tumblr data the front end might need
            blog_names = [blog.name for blog in user_info.user.blogs]
            
            tumblr_imports = {}
            
            for name in blog_names:
                blog_posts = []
                for post in client.posts(name, type='text').posts:
                    blog_posts.append({ 'title': post.title, 'tags': post.tags, 'body': post.body })
                
                tumblr_imports[name] = blog_posts
                
        # return Response(json.dumps(tumblr_imports), mimetype='application/json')
        return Response(tumblr_imports, mimetype='application/json')
    
        
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
#}

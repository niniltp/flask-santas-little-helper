from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_simple_captcha import CAPTCHA
from flask_talisman import Talisman
from livereload import Server

from app.policy.csp import csp

import os, datetime, logging

def redirect(e):
    return render_template('error.html')

def create_app():
    app = Flask(__name__)

    log = logging.getLogger('werkzeug')
    log.disabled = True
    
    from app import settings
    app.config['TEMPLATES_FOLDER'] = settings.TEMPLATES_FOLDER
    app.config['STATIC_FOLDER'] = settings.STATIC_FOLDER

    app.config['SECRET_KEY'] = os.urandom(24).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

    if os.environ['FLASK_LIVERELOAD'] != "False":
        app.config['FLASK_LIVERELOAD'] = True
    else:
        app.config['FLASK_LIVERELOAD'] = False
    

    app.register_error_handler(400, redirect)
    app.register_error_handler(401, redirect)
    app.register_error_handler(403, redirect)
    app.register_error_handler(404, redirect)
    app.register_error_handler(405, redirect)
    app.register_error_handler(500, redirect)
    app.register_error_handler(502, redirect)

    db.init_app(app)
    csrf.init_app(app)
    CAPTCHA.init_app(app)
    talisman = Talisman(app, 
        force_https=False, 
        strict_transport_security=False,
        strict_transport_security_include_subdomains=False,
        session_cookie_secure=False,
        frame_options='DENY',
        content_security_policy=csp        
    ) 
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)

    from .model.schema import User 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from app.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    from app.room import room as room_blueprint
    app.register_blueprint(room_blueprint, url_prefix='/room')

    from app.item import item as item_blueprint
    app.register_blueprint(item_blueprint, url_prefix='/room/list/item')

    return app

db = SQLAlchemy()
csrf = CSRFProtect()
CAPTCHA_CONFIG = {'SECRET_CSRF_KEY': os.urandom(24).hex()}
CAPTCHA = CAPTCHA(config=CAPTCHA_CONFIG)

app = create_app()

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    session.modified = True

if app.config['FLASK_LIVERELOAD']:
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve()
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from app.model.schema import User, Room, Item, Association, addObj
from app.checker import *
from app import CAPTCHA
import datetime

from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            captcha = CAPTCHA.create()
            return render_template('login.html', captcha=captcha)
        else:
            return redirect(url_for('profile.index'))
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if not CAPTCHA.verify(c_text, c_hash):
            flash('Captcha incorrect.')
            return redirect(url_for('main.login'))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('The information provided is incorrect.')
            return redirect(url_for('main.login'))

        login_user(user)
        session.permanent = True
        
        print(db.session.query(User).all())
        print(db.session.query(Room).all())
        print(db.session.query(Association).all())
        print(db.session.query(Item).all())

        return redirect(url_for('profile.index'))


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            captcha = CAPTCHA.create()
            return render_template('signup.html', captcha=captcha)    
        else:
            return redirect(url_for('room.index'))
    else:
        email = request.form.get('email').strip()
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if not CAPTCHA.verify(c_text, c_hash):
            flash('Captcha incorrect.')
            return redirect(url_for('main.signup'))

        code, msgError = check_email(email)
        if code != 0:
            flash(msgError)
            return redirect(url_for('main.signup'))

        code, msgError = check_name(name)
        if code != 0:
            flash(msgError)
            return redirect(url_for('main.signup'))

        code, msgError = check_password(password)
        if code != 0:
            flash(msgError)
            return redirect(url_for('main.signup'))

        if password != confirm_password :
            flash('The information provided is incorrect.')
            return redirect(url_for('main.signup'))

        new_user = User(email=email,\
            name=name,\
            password=generate_password_hash(password))

        if not addObj(new_user):
            flash('This account already exists.')
            return redirect(url_for('main.signup'))


    return redirect(url_for('main.login'))

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    isFalseError(current_user.is_authenticated)
    logout_user()

    session.permanent = False

    return redirect(url_for('.index'))
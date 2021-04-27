from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_required, current_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from app.model.schema import User, Room, Item, Association, addObj, deleteObj, commit
from app.checker import *
import datetime

from . import db

profile = Blueprint('profile', __name__)

@profile.route('/', methods=['GET'])
@login_required  
def index():
    return render_template('profile.html')

@profile.route('/edit', methods=['GET'])
@login_required
def edit():
    return render_template('profile/edit.html')

@profile.route('/edit/settings', methods=['POST'])
@login_required
def edit_settings():
    email = request.form.get('email').strip()
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if name:
        code, msgError = check_name(name)
        if code != 0:
            flash('#1' + msgError)
            return redirect(url_for('profile.edit'))
    
    if not check_password_hash(current_user.password, password)\
        or not check_password_hash(current_user.password, confirm_password):
        flash('#1The information provided is incorrect.')
        return redirect(url_for('profile.edit'))

    #if email:
    #    if not "@" in email:
    #        flash('#1Wrong email format provided.')
    #        return redirect(url_for('profile.edit'))

    if email:
        code, msgError = check_email(email)
        if code != 0:
            flash("#1" + msgError)
            return redirect(url_for('profile.edit'))

    if User.query.filter_by(email=email).first():
        flash('#1This account already exists.')
        return redirect(url_for('profile.edit'))

    user = User.query.filter_by(id=current_user.id).first()

    if email and email != user.email:
        user.email = email
    if name:
        user.name = name
    
    commit()

    return redirect(url_for('.index'))

@profile.route('/edit/password', methods=['POST'])
@login_required
def edit_password():

    password = request.form.get('password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    code, msgError = check_password(new_password)
    if code != 0:
        flash('#2' + msgError)
        return redirect(url_for('profile.edit'))

    if not password or not new_password or not confirm_password:
        flash('#2Invalid information provided')
        return redirect(url_for('profile.edit'))

    if not check_password_hash(current_user.password, password):
        flash('#2Invalid information provided')
        return redirect(url_for('profile.edit'))

    if new_password != confirm_password:
        flash('#2Invalid information provided')
        return redirect(url_for('profile.edit'))
    
    user = User.query.filter_by(id=current_user.id).first()

    user.password = generate_password_hash(new_password)
    commit()

    return redirect(url_for('profile.index'))


@profile.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'GET':
        return render_template('profile/delete.html')
    else:
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not check_password_hash(current_user.password, password)\
            or not check_password_hash(current_user.password, confirm_password):
            flash('Invalid information provided.')
            return redirect(url_for('profile.delete'))

        current_user.delete()
        commit()

        logout_user()
        session.permanent = False

        return redirect(url_for('main.index'))

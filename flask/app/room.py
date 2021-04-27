from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from app.model.schema import Room, User, Association, addObj, commit
from app.checker import *

from . import db

room = Blueprint('room', __name__)

@room.route('/', methods=['GET'])
@login_required
def index():
    return render_template('room.html')

@room.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET': 
        return render_template('room/create.html')
    else:
        name = request.form.get('name')
        secret = request.form.get('secret')
        
        code, msgError = check_room_name(name)
        if code != 0:
            flash(msgError)
            return redirect(url_for('room.create'))

        name = name + "#" + str(current_user.id)

        if secret:
            new_room = Room(name=name, secret=generate_password_hash(secret))
        else:
            new_room = Room(name=name)

        room = db.session.query(Association.room_id).join(Room).filter((Association.user_id == current_user.id) & (Room.name == name)).all()
        if room: 
            flash('A Room with this name already exists. Please choose another Room\'s name.')
            return redirect(url_for('room.create'))

        assoc = Association(role_id=0)
        assoc.room = new_room
        current_user.rooms.append(assoc)

        commit()


        return redirect(url_for('room.index'))

@room.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    if request.method == 'GET': 
        return render_template('room/join.html')
    else:
        name = request.form.get('name')
        secret = request.form.get('secret')
        
        queryRooms = db.session.query(Room.id, Room.name, Room.secret).all()
        if name not in [attr[1] for attr in queryRooms]:
            flash('Invalid information provided')
            return redirect(url_for('room.join'))

        room_id = [attr[0] for attr in queryRooms if attr[1] == name][0]

        assocQuery = db.session.query(Association.user_id)\
            .filter(Association.room_id == room_id).all()

        if current_user.id in [attr[0] for attr in assocQuery]:
            flash('You are already a member of this Room')
            return redirect(url_for('room.join'))

        room_secret = [attr[2] for attr in queryRooms if attr[1] == name][0]
        
        if room_secret:
            if not check_password_hash(room_secret, secret):
                flash('Invalid information provided')
                return redirect(url_for('room.join'))
        else:
            if secret:
                flash('Invalid information provided')
                return redirect(url_for('room.join'))
        
        assoc = Association(room_id=room_id,\
                user_id=current_user.id,\
                role_id=1)
        
        addObj(assoc)

        return redirect(url_for('room.index'))

@room.route('/edit', methods=['GET'])
@login_required
def edit():
    
    isNoneError(request.args.get('room_id'))
    room_id = isNotIntegerError(request.args.get('room_id'))

    isFalseError(current_user.isAdmin(room_id))
    isNoneError(current_user.isAdmin(room_id))
        
    for assoc in current_user.rooms:
        if assoc.room.id == int(room_id):
            return render_template('room/edit.html', room=assoc.room)



@room.route('/edit/name', methods=['POST'])
@login_required
def edit_name():

    name = request.form.get('name')
    secret = request.form.get('current_secret')
    confirm_secret = request.form.get('confirm_secret')

    isNoneError(request.form.get('room_id'))
    room_id = isNotIntegerError(request.form.get('room_id'))

    isFalseError(current_user.isAdmin(room_id))
    isNoneError(current_user.isAdmin(room_id))

    roomQuery = Room.query.join(Association)\
        .filter(Association.room_id==room_id)\
        .filter(Association.user_id==current_user.id)\
        .filter(Association.role_id==0).first()
    
    isNoneError(roomQuery) 

    code, msgError = check_room_name(name)
    if code != 0:
        flash('#1' + msgError)
        return redirect(url_for('room.edit', room_id=room_id))


    if roomQuery.secret:
        if not secret or not confirm_secret:
            flash('#1The information provided is incorrect.')
            return redirect(url_for('room.edit', room_id=room_id))

        if not check_password_hash(generate_password_hash(secret), confirm_secret)\
            or not check_password_hash(generate_password_hash(confirm_secret), secret):
            flash('#1The information provided is incorrect.')
            return redirect(url_for('room.edit', room_id=room_id))

        if not check_password_hash(roomQuery.secret, secret):
            flash('#1The information provided is incorrect.')
            return redirect(url_for('room.edit', room_id=room_id))

    roomQuery.name = name + "#" + str(current_user.id)
    commit()
    
    return redirect(url_for('room.index'))


@room.route('/edit/password', methods=['POST'])
@room.route('/edit/add-password', methods=['POST'])
@login_required
def edit_addpsw():

    password = request.form.get('password')
    secret = request.form.get('current_secret')
    new_secret = request.form.get('new_secret')
    confirm_secret = request.form.get('confirm_secret')

    isNoneError(request.form.get('room_id'))
    room_id = isNotIntegerError(request.form.get('room_id'))

    isFalseError(current_user.isAdmin(room_id))
    isNoneError(current_user.isAdmin(room_id))

    if not new_secret or not confirm_secret:
        flash('#2The information provided is incorrect.')
        return redirect(url_for('room.edit', room_id=room_id))
    
    #if not check_password_hash(current_user.password, password):
    if not check_password_hash(current_user.password, password):
        flash('#2The information provided is incorrect.')
        return redirect(url_for('room.edit', room_id=room_id))

    if not check_password_hash(generate_password_hash(new_secret), confirm_secret)\
        or not check_password_hash(generate_password_hash(confirm_secret), new_secret):
        flash('#2The information provided is incorrect.')
        return redirect(url_for('room.edit', room_id=room_id))

    roomQuery = Room.query.join(Association)\
        .filter(Association.room_id==room_id)\
        .filter(Association.user_id==current_user.id)\
        .filter(Association.role_id==0).first()

    if roomQuery.secret:
        if not secret:
            flash('#2The information provided is incorrect.')
            return redirect(url_for('room.edit', room_id=room_id))

        if not check_password_hash(roomQuery.secret, secret):
            flash('#2The information provided is incorrect.')
            return redirect(url_for('room.edit', room_id=room_id))

    roomQuery.secret = generate_password_hash(new_secret)

    commit()

    return redirect(url_for('room.index'))


@room.route('/edit/remove-password', methods=['POST'])
@login_required
def edit_removepsw():

    password = request.form.get('password')
    secret = request.form.get('current_secret')
    confirm_secret = request.form.get('confirm_secret')
    
    isNoneError(request.form.get('room_id'))
    room_id = isNotIntegerError(request.form.get('room_id'))

    isFalseError(current_user.isAdmin(room_id))
    isNoneError(current_user.isAdmin(room_id))

    if not password or not secret or not confirm_secret:
        flash('#3The information provided is incorrect.')
        return redirect(url_for('room.edit', room_id=room_id))

    if not check_password_hash(current_user.password, password):
        flash('#3The information provided is incorrect.')
        return redirect(url_for('room.edit', room_id=room_id))

    if not check_password_hash(generate_password_hash(secret), confirm_secret)\
        or not check_password_hash(generate_password_hash(confirm_secret), secret):
        flash('#3The information provided is incorrect.')
        return redirect(url_for('room.edit', room_id=room_id))

    roomQuery = Room.query.join(Association)\
        .filter(Association.room_id==room_id)\
        .filter(Association.user_id==current_user.id)\
        .filter(Association.role_id==0).first()

    if not check_password_hash(roomQuery.secret, secret):
        flash('#3The information provided is incorrect.')
        return redirect(url_for('room.edit', room_id=room_id))
    
    roomQuery.secret = None

    commit()

    return redirect(url_for('room.index'))

@room.route('/delete', methods=["POST"])
@login_required
def delete():

    isNoneError(request.form.get('room_id'))
    room_id = isNotIntegerError(request.form.get('room_id'))

    isFalseError(current_user.isAdmin(room_id))
    isNoneError(current_user.isAdmin(room_id))

    for assoc in current_user.rooms:
        if assoc.room.id == int(room_id):
            assoc.room.delete()

    return redirect(url_for('room.index'))

@room.route('/exit', methods=["POST"])
@login_required
def exit():

    isNoneError(request.form.get('room_id'))
    room_id = isNotIntegerError(request.form.get('room_id'))

    isTrueError(current_user.isAdmin(room_id))
    isNoneError(current_user.isAdmin(room_id))
        
    for assoc in current_user.rooms:
        if assoc.room.id == int(room_id):
            assoc.room.exit(current_user.id)
    
    return redirect(url_for('room.index'))
    
@room.route('/kick', methods=["POST"])
@login_required
def kick():

    isNoneError(request.form.get('room_id'))
    isNoneError(request.form.get('user_id'))

    room_id = isNotIntegerError(request.form.get('room_id'))
    user_id = isNotIntegerError(request.form.get('user_id'))

    isNoneError(current_user.isAdmin(room_id))
    isFalseError(current_user.isAdmin(room_id))

    user_to_kick = current_user.getUserByID(user_id)

    isNoneError(user_to_kick.isAdmin(room_id))
    isTrueError(user_to_kick.isAdmin(room_id))
 
    for assoc in current_user.rooms:
        if assoc.room.id == int(room_id):
            assoc.room.exit(user_id)

    
    return redirect(url_for('item.list_', room_id=room_id))
    
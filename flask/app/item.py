from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, current_user
from app.model.schema import User, Room, Item, addObj, deleteObj, commit
from app.checker import *

from . import db

item = Blueprint('item', __name__)

@item.route('/', methods=['GET'])
@login_required
def list_():

    isNoneError(request.args.get('room_id'))
    room_id = isNotIntegerError(request.args.get('room_id'))

    isNoneError(current_user.isAdmin(room_id))
    
    for assoc in current_user.rooms:
        if assoc.room.id == int(room_id):
            return render_template('item/list.html', room=assoc.room)
    return render_template('room.html', user=current_user)


@item.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':

        isNoneError(request.args.get('room_id'))
        room_id = isNotIntegerError(request.args.get('room_id'))
        isNoneError(current_user.isAdmin(room_id))

        return render_template('item/create.html', room=[assoc.room for assoc in current_user.rooms if assoc.room.id == room_id][0])
    else:        
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        url = request.form.get('url')

        isNoneError(request.form.get('room_id'))
        room_id = isNotIntegerError(request.form.get('room_id'))
        isNoneError(current_user.isAdmin(room_id))
                
        code, msgError = check_item_name(name)
        if code != 0:
            flash(msgError)
            return redirect(url_for('item.create', room_id=room_id))

        if not checkNumberInput(price) or not checkNumberInput(quantity):
            flash('A positive number is required for a quantity and a price.')
            return redirect(url_for('item.create', room_id=room_id))
        
        item = Item(\
                name=name,\
                price=price,\
                quantity=quantity,\
                url=url,\
                rid=room_id,\
                uid=current_user.id,\
                gid=None,\
            )

        addObj(item)

        return redirect(url_for('item.list_', room_id=room_id))

@item.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':

        isNoneError(request.args.get('room_id'))
        isNoneError(request.args.get('item_id'))

        room_id = isNotIntegerError(request.args.get('room_id'))
        item_id = isNotIntegerError(request.args.get('item_id'))

        isNoneError(current_user.isAdmin(room_id))
        isFalseError(current_user.ownItem(room_id, item_id))

        return render_template('item/edit.html',\
                    item=Item.query.get(item_id),\
                    room=[assoc.room for assoc in current_user.rooms if assoc.room.id == room_id][0])
    else:
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        url = request.form.get('url')
        
        isNoneError(request.form.get('room_id'))
        isNoneError(request.form.get('item_id'))

        room_id = isNotIntegerError(request.form.get('room_id'))
        item_id = isNotIntegerError(request.form.get('item_id'))

        isNoneError(current_user.isAdmin(room_id))
        isFalseError(current_user.ownItem(room_id, item_id))

        code, msgError = check_item_name(name)
        if code != 0:
            flash(msgError)
            return redirect(url_for('item.edit', room_id=room_id, item_id=item_id))

        if not name and not quantity and not url and not price:
            flash('At least one value in the fields is required to edit the item.')
            return redirect(url_for('item.edit', room_id=room_id, item_id=item_id))

        if not checkNumberInput(price) or not checkNumberInput(quantity):
            flash('A positive number is required for a quantity and a price.')
            return redirect(url_for('item.edit', room_id=room_id, item_id=item_id))
                
        item = Item.query.get(item_id)

        if item:
            if name:
                item.name = name
            if price:
                item.price = price 
            if quantity:
                item.quantity = quantity
            if url:
                item.url = url
        else:
            flash('The item to edit was not found. Please try later.')
            return redirect(url_for('item.edit', room_id=room_id, item_id=item_id))
        
        commit()

        return redirect(url_for('item.list_', room_id=room_id))

@item.route('/delete', methods=['POST'])
@login_required
def delete():    
    isNoneError(request.form.get('room_id'))
    isNoneError(request.form.get('item_id'))

    room_id = isNotIntegerError(request.form.get('room_id'))
    item_id = isNotIntegerError(request.form.get('item_id'))

    isNoneError(current_user.isAdmin(room_id))
    isFalseError(current_user.ownItem(room_id, item_id))
    
    item = Item.query.get(item_id)

    if item:
        deleteObj(item)

    return redirect(url_for('item.list_', room_id=room_id))


@item.route('/gift', methods=['POST'])
@login_required
def gift():

    isNoneError(request.form.get('room_id'))
    isNoneError(request.form.get('item_id'))

    room_id = isNotIntegerError(request.form.get('room_id'))
    item_id = isNotIntegerError(request.form.get('item_id'))

    isNoneError(current_user.isAdmin(room_id)) # checks that the user is member of the room
    isTrueError(current_user.ownItem(room_id, item_id)) # checks that the user is not the owner

    item = Item.query.get(item_id)       

    if item:
        if item.gid is None:
            item.gid = current_user.id # becomes the gifter
        else:
            if current_user.id == item.gid:
                item.gid = None
            else:
                abort(403)

        commit()
    
    return redirect(url_for('item.list_', room_id=room_id))
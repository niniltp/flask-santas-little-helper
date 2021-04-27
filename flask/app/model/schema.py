from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc

from app import db

def addObj(obj):
    try:
        db.session.add(obj)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False

def deleteObj(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False

def commit():
    db.session.commit()

class Association(db.Model):

    __tablename__ = "association"
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)

    room = db.relationship("Room", back_populates="users")
    user = db.relationship("User", back_populates="rooms")
    
    def __repr__(self):
        return '<Association %r %r %r>' % (self.room_id, self.user_id, self.role_id)

class Room(db.Model):
    __tablename__ = 'room'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    secret = db.Column(db.String(100), nullable=True)
    users = db.relationship('Association', back_populates='room')

    def __repr__(self):
        return '<Room %r %r>' % (self.id, self.name)

    def deleteAllItems(self):
        for item in Item.query.filter_by(rid=self.id).all():
            deleteObj(item)


    def deleteUserItems(self, user_id):
        if user_id:
            for item in Item.query.filter(Item.uid==user_id).filter(Item.rid==self.id).all():
                deleteObj(item)
            for item in Item.query.filter(Item.gid==user_id).filter(Item.rid==self.id).all():
                item.gid = None

    def delete(self):
        room = Room.query.get(self.id)
        if room:
            for association in room.users:
                deleteObj(association)
            room.deleteAllItems()
            deleteObj(room)            
        commit()

    def exit(self, user_id):
        self.deleteUserItems(user_id) 
        Association.query\
            .filter(Association.user_id == user_id)\
            .filter(Association.room_id == self.id).delete()
        commit()

    def getRoomByID(self):
        return Room.query.filter_by(id=self.id).first()

    def getNbUsers(self):
        return db.session.query(Association.user_id).filter(Association.room_id== self.id).count()
    
    def getUserItems(self, user_id):
        return db.session.query(Item)\
            .filter((Item.rid == self.id) &\
                    (Item.uid == user_id)).all()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False) 
    rooms = db.relationship('Association', back_populates='user')

    def __repr__(self):
        return '<User %r %r>' % (self.id, self.email)
    
    def isAdmin(self, room_id):
        if db.session.query(Association.role_id)\
            .filter(Association.user_id == self.id)\
            .filter(Association.room_id == room_id).scalar() == 0:
            return True
        elif db.session.query(Association.role_id)\
            .filter(Association.user_id == self.id)\
            .filter(Association.room_id == room_id).scalar() == 1:
            return False
        else:
            return None

    def ownItem(self, room_id, item_id):
        item = Item.query.get(item_id)

        if not item:
            return False
        else:
            if item.rid == room_id and item.uid == self.id:
                return True
            else:
                return False
    
    def delete(self):
        user = User.query.get(self.id)
        if user:
            for association in user.rooms:
                room = self.getRoomByID(association.room_id)
                if association.role_id == 0:                    
                    room.delete()     
                else:
                    room.deleteUserItems(self.id) 
                deleteObj(association)
            deleteObj(user)  

    def getRoomByID(self, room_id):
        return db.session.query(Room).join(Association)\
            .filter(Association.room_id==room_id)\
            .filter(Association.user_id==self.id).first()
    
    def getUserByID(self, user_id):
        return User.query.filter_by(id=user_id).first()
    
class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(1000), nullable=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rid = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    gid = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
            return '<Item %r %r %r %r %r %r %r>' % (self.name, self.price, self.quantity, self.url, self.rid, self.uid, self.gid)
from flask import abort
import re

def check_room_name(name):
    code = 0
    msgError = ""

    pattern = re.compile("^[a-zA-Z0-9~_.-]*$")

    if not name:
        msgError += "Room name is empty. "
        code = 1
    if not bool(pattern.search(name)):
        msgError += "Forbidden characters detected. "
        code = 1
    if len(name) < 4:
        msgError += "Must be more than 4 characters. "
        code = 1
    if len(name) > 20:
        msgError += "Must be less than 20 characters. "
        code = 1
    
    return code, msgError

def check_name(name):
    code = 0
    msgError = ""

    pattern = re.compile("^[a-zA-Z0-9_.-]*$")

    if not name:
        msgError += "Name is empty. "
        code = 1
    if not bool(pattern.search(name)):
        msgError += "Forbidden characters detected in name. "
        code = 1
    if len(name) < 2:
        msgError += "Name must be more than 2 characters. "
        code = 1
    if len(name) > 20:
        msgError += "Name must be less than 20 characters. "
        code = 1
    
    return code, msgError

def check_email(email):
    code = 0
    msgError = ""

    pattern = re.compile("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}$", re.I)

    if not email:
        msgError += "Email is empty. "
        code = 1
    if not bool(pattern.search(email)):
        msgError += "Wrong email format. "
        code = 1
    if len(email) > 256:
        msgError += "Email too long. "
        code = 1

    return code, msgError


def check_password(password):
    code = 0
    msgError = ""

    if not password:
        msgError += "Password is empty. "
        code = 1
    else:
        if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,30}$", password):
            msgError += "Password must have be at least 8 characters long and have at least one uppercase, digit and special character"
            code = 1
    
    return code, msgError

def check_item_name(name):
    code = 0
    msgError = ""

    pattern = re.compile('^[a-zA-Z0-9!@$%^&*()_+\-=\[\];:"\\| ,.\/?]*$')

    if not name:
        msgError += "Name is empty. "
        code = 1
    if not bool(pattern.search(name)):
        msgError += "Forbidden characters detected in name. "
        code = 1
    if len(name) < 1:
        msgError += "Name must be more than 1 character. "
        code = 1
    if len(name) > 40:
        msgError += "Name must be less than 40 characters. "
        code = 1
    
    return code, msgError









def isNotIntegerError(_input):
    try:
        _integer = int(_input)
        return _integer
    except:
        abort(404)

def isFalseError(_input):
    if _input is False or _input == 0:
        abort(404)

def isNoneError(_input):
    if _input is None:
        abort(404)

def isNotNoneError(_input):
    if _input is not None:
        abort(404)

def isTrueError(_input):
    if _input:
        abort(404)

def checkNumberInput(input):
    if input:
        try: 
            if not int(input):
                return 0
            if int(input) < 0:
                return 0
            return 1
        except ValueError:
            return 0
    else:
        return 1
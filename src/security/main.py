from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, status, HTTPException


security = HTTPBasic()

users = {
    'admin': {
        'username': 'admin',
        'password': 'hugebbc'
    }
}

def verification(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    if username in users and password == users[username]['password']:
        return True
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'}
        )
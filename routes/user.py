# Python
from typing import List

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import status, HTTPException

# User models
from tables.user import users
from models.user import UserBase, UserOut, UserRegister

# Database
from config.db import conn

# Encryption
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key=key)


user = APIRouter()


def get_user_by_ID(id: int):
    user = conn.execute(users.select().where(users.c.id == id)).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User ID not found'
        )


def encrypt(string: str):
    return f.encrypt(string.encode('utf-8'))


# Path operations

## Register a user
@user.post(
    path='/users/new',
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary='Create User',
    tags=['users']
)
def create_user(user: UserRegister = Body(...)):
    '''
    Create User

    This path operation creates a user and saves it to the database

    Parameters:
    - Request Body parameters:
        - user: UserRegister

    Returns a json of the user with the following structure:
        - id: int
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: Optional[date]
    '''
    new_user = dict(user)

    new_user['password'] = encrypt(new_user['password'])

    result = conn.execute(users.insert(new_user))

    return get_user_by_ID(result.lastrowid)


## Show all users
@user.get(
    path='/users',
    response_model=List[UserOut],
    status_code=status.HTTP_200_OK,
    summary='Show all users',
    tags=['users']
)
def show_all_users():
    '''
    Show all users

    This path operation shows all the users of the app database

    Parameters:
    -

    Returns a json list with the of the users with the following keys:
    - id: int
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: Optional[date]
    '''
    return conn.execute(users.select()).all()


## Show a user
@user.get(
    path='/users/{user_id}',
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary='Show a user',
    tags=['users']
)
def show_user(user_id: int = Path(...)):
    '''
    Show user

    This path operation shows the user with the given ID

    Parameters:
    - Path parameters:
        - user_id: int
    
    Returns a json of the user with the following keys:
    - id: int
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: Optional[date]
    '''
    return get_user_by_ID(user_id)


@user.delete(
    path='/users/delete/{user_id}',
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary='Delete User',
    tags=['users']
)
def delete_user(user_id: int = Path(...)):
    '''
    Delete User

    This path operation deletes a user

    Parameters:
    - Path parameters:
        - user_id: int
    
    Returns a json of the deleted user with the following keys:
    - id: int
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: Optional[date]
    '''
    deleted_user = get_user_by_ID(user_id)

    conn.execute(users.delete().where(users.c.id == user_id))

    return deleted_user

## Update user
@user.put(
    path='/users/update/{user_id}',
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary='Update user',
    tags=['users']
)
def update_user(user_id: int = Path(...), user: UserBase = Body(...)):
    '''
    Update user

    This path operation updates a user

    Parameters:
    - Path parameters:
        - user_id: int
    - Request Body parameters:
        - user: UserBase
    
    Returns a json of the updated user with the following keys:
    - id: int
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: Optional[date]
    '''
    updated_user = dict(user)

    conn.execute(users.update().where(users.c.id == user_id).values(
        email=updated_user['email'],
        first_name=updated_user['first_name'],
        last_name=updated_user['last_name'],
        birth_date=updated_user['birth_date']
    ))

    return get_user_by_ID(user_id)
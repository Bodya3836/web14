import datetime
import jwt

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from depenedencies.database import get_db, SessionLocal

from services.users import UserService
from schemas.user import User, RolesEnum


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

secret_key = "secret_key"



class Token(BaseModel):
    access_token: str | bytes
    token_type: str = "bearer"


def create_access_token(username: str, role: str):
    """
    The create_access_token function creates a JWT token with the following claims:
        - sub (subject): The username of the user who is logging in.
        - role: The role of the user who is logging in.
        - exp (expiration time): A datetime object that indicates when this token will expire.
    
    :param username: str: Specify the username of the user that is being created
    :param role: str: Define the role of the user
    :return: A token
    :doc-author: Trelent
    """
    token_data = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(token_data, secret_key, algorithm="HS256")

    return token

def decode_jwt_token(token):
        """
        The decode_jwt_token function takes in a token and returns the decoded payload.
            If the token is expired, it will return &quot;The token has already expired&quot;.
            If the signature of the token is invalid, it will return &quot;Invalid Token&quot;.
        
        :param token: Pass the token to be decoded
        :return: The decoded payload
        :doc-author: Trelent
        """
        try:
            decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            return "The token has already expired"
        except jwt.InvalidTokenError:
            return "Invalid token"



async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the UserResource class.
        It takes a token as an argument and returns the user object associated with that token.
        
        :param token: str: Get the token from the request header
        :param db: SessionLocal: Get the database connection
        :return: The user object
        :doc-author: Trelent
        """
        token = decode_jwt_token(token)
        user_service = UserService(db)
        username = token.get("sub")
        user = user_service.get_by_username(username)

        return user

async def check_is_admin(user: User = Depends(get_current_user)) -> User:
    """
    The check_is_admin function is a dependency that checks if the user has admin privileges.
    If they do, it returns the user object. If not, it raises an HTTPException with status code 403.
    
    :param user: User: Get the current user
    :return: The user object if the role is admin and confirmed
    :doc-author: Trelent
    """
    if user.role == RolesEnum.ADMIN and user.confirmed:
        return user
    raise HTTPException(status_code=403)

async def check_is_default_user(user: User = Depends(get_current_user)) -> User:
    """
    The check_is_default_user function is a dependency that checks if the user has one of the following roles:
        - USER
        - MANAGER
        - ADMIN
    and also checks if they are confirmed. If so, it returns the user object. Otherwise, it raises an HTTPException with a 403 status code.
    
    :param user: User: Get the user object from the database
    :return: The user object if the user is not a default one
    :doc-author: Trelent
    """
    if user.role in [RolesEnum.USER, RolesEnum.MANAGER, RolesEnum.ADMIN] and user.confirmed:
        return user
    raise HTTPException(status_code=403)

async def check_is_manager(user: User = Depends(get_current_user)) -> User:
    """
    The check_is_manager function checks if the user is a manager or admin.
        If so, it returns the user object. Otherwise, it raises an HTTPException with status code 403.
    
    :param user: User: Get the current user from the database
    :return: A user object
    :doc-author: Trelent
    """
    if user.role in [RolesEnum.MANAGER, RolesEnum.ADMIN]:
        return user
    raise HTTPException(status_code=403)

def create_email_token(self, data: dict):
        """
        The create_email_token function takes a dictionary of data and returns a JWT token.
            The token is encoded with the SECRET_KEY and ALGORITHM defined in the class.
            The iat (issued at) claim is set to datetime.utcnow() and exp (expiration time) 
            claim is set to 7 days from now.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass the data to be encoded
        :return: A token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

async def get_email_from_token(self, token: str):
  """
  The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
  If the token is invalid, it raises an HTTPException.
  
  :param self: Represent the instance of the class
  :param token: str: Pass in the token that is sent to the user's email
  :return: The email address that was encoded in the token
  :doc-author: Trelent
  """
  try:
      payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
      email = payload["sub"]
      return email
  except JWTError as e:
      print(e)
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                          detail="Invalid token for email verification")

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm


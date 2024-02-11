from fastapi import APIRouter, Depends, HTTPException, status, Security, BackgroundTasks, Request, File, UploadFile
from depenedencies.database import get_db, SessionLocal
from depenedencies.auth import Token, create_access_token, get_current_user
from schemas.user import User, UserConfirmed
from services.users import UserService
from services.email import send_email
from fastapi.security import OAuth2PasswordRequestForm

from depenedencies.rate_limiter import RateLimiter
from depenedencies.cloudinary_client import get_uploader


router = APIRouter()

rate_limiter = RateLimiter(3, 120)

async def rate_limit(request: Request):
    """
    The rate_limit function is a middleware function that will be called before every request.
    It checks if the client has exceeded their rate limit, and if so, raises an HTTPException with status code 429 (Too Many Requests).
    If the client hasn't exceeded their rate limit, it returns True to indicate that the request should proceed as normal.
    
    :param request: Request: Get the client id from the request object
    :return: True if the client is allowed to make a request, and raises an exception otherwise
    :doc-author: Trelent
    """
    global rate_limiter
    client_id = request.client.host
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(status_code=429, detail="Too Many Requests")
    return True




@router.post("/register", response_model=User)
async def register(user: User, db: SessionLocal = Depends(get_db)):
    """
    The register function creates a new user in the database.
    
    :param user: User: Pass the user object to the function
    :param db: SessionLocal: Get the database connection
    :return: A user object, but it's not the same as the one you pass in
    :doc-author: Trelent
    """
    user_service = UserService(db=db)
    return user_service.create_new(user)

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    """
    The login_for_access_token function is used to obtain an access token for a user.
        The function takes in the username and password of the user, and returns an access token if successful.
    
    :param form_data: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: SessionLocal: Get the database connection
    :return: A dictionary with the access token and its type
    :doc-author: Trelent
    """
    user_service = UserService(db)
    user = user_service.get_user_for_auth(form_data.username, form_data.password)
    access_token = create_access_token(username = user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-resource/", response_model=User)
async def protected_resource(current_user: User = Depends(get_current_user)):
    """
    The protected_resource function is a protected resource that requires authentication.
    It returns the current user's details.
    
    :param current_user: User: Get the user object from the database
    :return: The current user
    :doc-author: Trelent
    """
    return current_user



@router.post('/confirmed/', response_model=User)
async def confirmed(data: UserConfirmed, db: SessionLocal = Depends(get_db)):
    """
    The confirmed function is used to confirm a user's email address.
        It takes in the UserConfirmed data model and returns a User object.
    
    :param data: UserConfirmed: Get the data from the user
    :param db: SessionLocal: Pass the database session to the user service
    :return: A user object
    :doc-author: Trelent
    """
    user_service = UserService(db)
    return user_service.confirmed_user(data)

@router.post("/upload_image")
def upload(current_user: User = Depends(get_current_user), file: UploadFile = File(...),  uploader = Depends(get_uploader), db: SessionLocal = Depends(get_db)):
    """
    The upload function is used to upload a file to the cloudinary server.
        The function takes in a file and an uploader object, which is used to 
        send the contents of the file up to cloudinary. Once uploaded, it returns
        a url that can be used by other functions.
    
    :param current_user: User: Get the current user in order to update their image
    :param file: UploadFile: Get the file from the request
    :param uploader: Upload the file to cloudinary
    :param db: SessionLocal: Get the database session
    :return: The following:
    :doc-author: Trelent
    """
    try:
        current_user
        user_service = UserService(db)
        contents = file.file.read()
        responce = uploader.upload(contents, public_id=file.filename)
        responce.get('secure_url')
        user_service.set_image(current_user, responce.get('secure_url'))

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
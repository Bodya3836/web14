from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status, Request
from pathlib import Path
import uvicorn
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr, BaseModel
from typing import List
from api.todo_items import router as todo_router
from api.users import router as user_router
from models import todo
from depenedencies.database import engine, get_db, SessionLocal
from schemas.user import Email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://www.anotherdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME="andriiok@meta.ua",
    MAIL_PASSWORD="secretPassword_",
    MAIL_FROM="andriiok@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Andriiok email",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

todo.Base.metadata.create_all(bind=engine)



app.include_router(todo_router, prefix="/todo")
app.include_router(user_router, prefix="/users")




@app.get("/")
async def health_check():
    """
    The health_check function is a simple function that returns the string &quot;OK&quot;
        to indicate that the server is running. This can be used by external services
        to check if this service is up and running.
    
    :return: A dictionary with the key &quot;ok&quot; and value true
    :doc-author: Trelent
    """
    print()
    return {"OK": True}

@app.post("/get_access_token")
async def complete_google_login(login: Email, db: SessionLocal = Depends(get_db)):
    """
    The complete_google_login function is used to complete the Google login process.
    It takes in a user's email address and returns an access token that can be used for authentication.
    
    :param login: Email: Pass the email address of the user to this function
    :param db: SessionLocal: Get the database session
    :return: A dictionary with the access token and its type
    :doc-author: Trelent
    """
    user_service = UserService(db)
    user = user_service.get_by_username(login.email)
    access_token = create_access_token(username = user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    """
    The send_in_background function sends an email in the background.
    
    :param background_tasks: BackgroundTasks: Add a task to the background tasks
    :param body: EmailSchema: Get the email address from the request body
    :return: A dictionary with the key &quot;message&quot; and value &quot;email has been sent&quot;
    :doc-author: Trelent
    """
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)




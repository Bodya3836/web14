from fastapi import APIRouter, Depends
from schemas.todo import Todo, TodoCreate, TodoUpdate
from depenedencies.database import get_db, SessionLocal
from services.todos import TodoService
from schemas.user import User

from depenedencies.auth import check_is_manager, check_is_admin, check_is_default_user

router = APIRouter()


@router.get("/")
async def list_todos(user: User = Depends(check_is_default_user), db: SessionLocal = Depends(get_db)) -> list[Todo]:
    """
    The list_todos function returns a list of all todo items in the database.
        
    
    :param user: User: Pass the user object to the function
    :param db: SessionLocal: Pass the database session to the todoservice
    :return: A list of todo objects
    :doc-author: Trelent
    """
    todo_items = TodoService(db=db).get_all_todos()
    return todo_items


@router.get("/{id}")
async def get_detail(id: int, user: User = Depends(check_is_default_user), db: SessionLocal = Depends(get_db)) -> Todo:
    """
    The get_detail function returns a single Todo item by id.
        
    
    :param id: int: Specify the id of the todo item that we want to get
    :param user: User: Get the user from the request
    :param db: SessionLocal: Get the database session
    :return: A todo object
    :doc-author: Trelent
    """
    todo_item = TodoService(db=db).get_by_id(id)
    return todo_item


@router.post("/")
async def create_todo( todo_item: TodoCreate, admin: User = Depends(check_is_admin), db: SessionLocal = Depends(get_db)) -> Todo:
    """
    The create_todo function creates a new todo item.
        The function takes in the following parameters:
            - todo_item: A TodoCreate object containing the information for creating a new todo item.
            - admin: An optional User object that contains information about an authenticated user (if any). This is used by FastAPI's Depends() decorator, which checks if the user is an admin before allowing them access to this endpoint. If no user is provided, then it will return None and not check anything else. 
            - db: An optional SessionLocal object that contains database connection info (if any).
    
    :param todo_item: TodoCreate: Pass in the todocreate object that is passed into the function
    :param admin: User: Check if the user is an admin
    :param db: SessionLocal: Get the database session from the dependency injection
    :return: A todo object, which is defined in the schemas
    :doc-author: Trelent
    """
    new_item = TodoService(db=db).create_new(todo_item)
    return new_item


@router.put("/{id}")
async def update_todo(id: int, todo_item: TodoUpdate, db: SessionLocal = Depends(get_db)) -> Todo:
    """
    The update_todo function updates a todo item in the database.
        The function takes an id and a TodoUpdate object as input, and returns the updated Todo object.
    
    :param id: int: Specify the id of the todo item that is being updated
    :param todo_item: TodoUpdate: Get the updated todo item from the request body
    :param db: SessionLocal: Pass the database session to the todoservice class
    :return: A todo object
    :doc-author: Trelent
    """
    updated_item = TodoService(db=db).update(todo_item)
    return updated_item

@router.delete("/")
async def remove_todo(id: int, db: SessionLocal = Depends(get_db)):
    """
    The remove_todo function removes a todo item from the database.
        Args:
            id (int): The ID of the todo item you want removed.
            db (SessionLocal): A connection to the database.
        Returns:
            TodoItem: The deleted TodoItem object.
    
    :param id: int: Specify that the id parameter is an integer
    :param db: SessionLocal: Pass the database session to the todoservice class
    :return: A todo object
    :doc-author: Trelent
    """
    todo_item = TodoService(db=db).remove(todo_item)
    return todo_item

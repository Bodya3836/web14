from repository.todos import TodoRepo
from schemas.todo import Todo, TodoCreate


class TodoService():
    def __init__(self, db) -> None:
        """
        The __init__ function is the constructor for a class.
        It's called when an instance of the class is created.
        The self parameter refers to the newly created object; it gives 
        the individual instance (rather than the class) access to 
        the attributes and methods in the class.
        
        :param self: Represent the instance of the class
        :param db: Pass the database connection to the repository
        :return: Nothing, so it returns none
        :doc-author: Trelent
        """
        self.repository = TodoRepo(db=db)

    def get_all_todos(self) -> list[Todo]:
        """
        The get_all_todos function returns a list of all todos in the database.
            :return: A list of Todo objects, each representing a single todo item.
        
        
        :param self: Represent the instance of the class
        :return: A list of todo objects
        :doc-author: Trelent
        """
        all_todos_from_db = self.repository.get_all() # list[TodoDB]
        result = [Todo.from_orm(item) for item in all_todos_from_db]
        return result

    def create_new(self, todo_item: TodoCreate) -> Todo:
        """
        The create_new function creates a new todo item.
            Args:
                todo_item (TodoCreate): The TodoCreate object containing the data for the new item.
            Returns:
                Todo: A Todo object representing the newly created item.
        
        :param self: Represent the instance of the class
        :param todo_item: TodoCreate: Create a new todo item
        :return: A todo object
        :doc-author: Trelent
        """
        new_item_from_db = self.repository.create(todo_item)
        todo_item = Todo.from_orm(new_item_from_db)
        return todo_item

    def get_by_id(self, id: int) -> Todo:
        """
        The get_by_id function returns a Todo object with the given id.
            
        
        :param self: Represent the instance of the class
        :param id: int: Specify the id of the todo item we want to get
        :return: The todo object
        :doc-author: Trelent
        """
        todo_item = self.repository.get_by_id(id)
        return Todo.from_orm(todo_item)
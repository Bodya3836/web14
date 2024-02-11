import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.todo import TodoDB
from app.repository.todos import TodoRepo

class TestTodoRepo(unittest.TestCase):
    def setUp(self):

        engine = create_engine('sqlite:///./test.db')
        self.mock_db = sessionmaker(bind=engine)()
        self.todo_repo = TodoRepo(db=self.mock_db)

    def test_get_all(self):
        # Ensure that the get_all method returns a list of TodoDB objects
        result = self.todo_repo.get_all()
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], TodoDB) if result else None

    def test_create_todo_item(self):
        # Ensure that a new TodoDB item is created and stored in the database
        todo_data = {"title": "Test Todo", "description": "Test Description"}
        new_item = self.todo_repo.create(todo_data)
        self.assertIsNotNone(new_item.id)
        self.assertEqual(new_item.title, todo_data["title"])

    def test_get_by_id(self):
        # Ensure that get_by_id method returns the correct TodoDB item
        todo_data = {"title": "Test Todo", "description": "Test Description"}
        new_item = self.todo_repo.create(todo_data)

        retrieved_item = self.todo_repo.get_by_id(new_item.id)
        self.assertEqual(retrieved_item.id, new_item.id)
        self.assertEqual(retrieved_item.title, new_item.title)

    def test_get_by_id_nonexistent(self):
        # Ensure that get_by_id method returns None for non-existent id
        non_existent_id = 999999
        retrieved_item = self.todo_repo.get_by_id(non_existent_id)
        self.assertIsNone(retrieved_item)

if __name__ == "__main__":
    unittest.main()

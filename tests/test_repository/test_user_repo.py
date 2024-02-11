import unittest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.users import UserDB
from app.dependencies.database import SessionLocal
from app.repository.user import UserRepo

class TestUserRepo(unittest.TestCase):
    def setUp(self):
        # Mocking the database or any dependencies
        engine = create_engine('sqlite:///:memory:')
        self.mock_db = sessionmaker(bind=engine)()
        self.user_repo = UserRepo(db=self.mock_db)

    def test_create_user(self):
        user_data = {"username": "testuser", "password": "password"}
        new_user = self.user_repo.create(user_data)
        self.assertIsNotNone(new_user.id)
        self.assertEqual(new_user.username, user_data["username"])

    def test_update_user(self):
        user_data = {"username": "testuser", "password": "password"}
        new_user = self.user_repo.create(user_data)

        updated_user_data = {"username": "updateduser", "password": "newpassword"}
        updated_user = self.user_repo.update(UserDB(**updated_user_data))

        self.assertIsNone(self.user_repo.get_by_username(user_data["username"]))
        self.assertIsNotNone(self.user_repo.get_by_username(updated_user_data["username"]))

    def test_get_by_username(self):
        user_data = {"username": "testuser", "password": "password"}
        new_user = self.user_repo.create(user_data)

        retrieved_user = self.user_repo.get_by_username(user_data["username"])
        self.assertEqual(retrieved_user.username, user_data["username"])

    def test_get_user_and_check_pass_success(self):
        user_data = {"username": "testuser", "password": "password"}
        new_user = self.user_repo.create(user_data)

        retrieved_user = self.user_repo.get_user_and_check_pass(user_data["username"], user_data["password"])
        self.assertEqual(retrieved_user.username, user_data["username"])

    def test_get_user_and_check_pass_failure(self):
        user_data = {"username": "testuser", "password": "password"}
        new_user = self.user_repo.create(user_data)

        retrieved_user = self.user_repo.get_user_and_check_pass(user_data["username"], "wrongpassword")
        self.assertIsNone(retrieved_user)

    def test_generate_salt(self):
        salt = self.user_repo.generate_salt()
        self.assertIsNotNone(salt)

    def test_hash_password(self):
        password = "password"
        hashed_password, salt = self.user_repo.hash_password(password)
        self.assertIsNotNone(hashed_password)
        self.assertIsNotNone(salt)

if __name__ == "__main__":
    unittest.main()

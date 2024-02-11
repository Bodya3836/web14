import unittest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from app.services.users import UserService, User, UserConfirmed


class TestUserService(unittest.TestCase):
    def setUp(self):
        # Mocking the database or any dependencies
        self.mock_db = Mock()
        self.user_service = UserService(db=self.mock_db)

    def test_create_new_user(self):
        user = User(username="testuser", password="password")
        with patch("your_module.send_email") as mock_send_email:
            new_user = self.user_service.create_new(user)
            mock_send_email.assert_called_once_with("Welcome", f"your code is {user.otp}", user.username)
            self.assertFalse(new_user.confirmed)  # Assuming confirmed is initially False

    def test_confirmed_user_success(self):
        user = User(username="testuser", password="password", otp="123456")
        confirmed_data = UserConfirmed(email=user.username, otp=user.otp)
        with patch.object(self.user_service.repository, "get_by_username", return_value=user):
            updated_user = self.user_service.confirmed_user(confirmed_data)
            self.assertTrue(updated_user.confirmed)

    def test_confirmed_user_failure(self):
        user = User(username="testuser", password="password", otp="123456")
        confirmed_data = UserConfirmed(email=user.username, otp="wrongotp")
        with patch.object(self.user_service.repository, "get_by_username", return_value=user):
            updated_user = self.user_service.confirmed_user(confirmed_data)
            self.assertFalse(updated_user.confirmed)

    def test_get_user_for_auth_success(self):
        user = User(username="testuser", password="password")
        with patch.object(self.user_service.repository, "get_user_and_check_pass", return_value=user):
            authenticated_user = self.user_service.get_user_for_auth(username=user.username, password=user.password)
            self.assertEqual(authenticated_user, user)

    def test_get_user_for_auth_failure(self):
        with patch.object(self.user_service.repository, "get_user_and_check_pass", return_value=None):
            with self.assertRaises(HTTPException) as context:
                self.user_service.get_user_for_auth(username="nonexistentuser", password="wrongpassword")
            self.assertEqual(context.exception.status_code, 403)

    def test_get_by_username_success(self):
        user = User(username="testuser", password="password")
        with patch.object(self.user_service.repository, "get_by_username", return_value=user):
            retrieved_user = self.user_service.get_by_username(username=user.username)
            self.assertEqual(retrieved_user, user)

    def test_get_by_username_failure(self):
        with patch.object(self.user_service.repository, "get_by_username", return_value=None):
            with self.assertRaises(HTTPException) as context:
                self.user_service.get_by_username(username="nonexistentuser")
            self.assertEqual(context.exception.status_code, 403)

    def test_set_image(self):
        user = User(username="testuser", password="password")
        url = "https://example.com/image.jpg"
        with patch.object(self.user_service.repository, "update") as mock_update:
            updated_user = self.user_service.set_image(user, url)
            self.assertEqual(updated_user.image, url)
            mock_update.assert_called_once_with(user)



from unittest.mock import patch

import app.repository.user
from app.services.users import UserService
from app.schemas.user import User, RolesEnum

from app.models.users import UserDB

def test_create_success(default_user, test_db):
    user_service = UserService(test_db)
    with patch(app.repository.user.UserRepo) as mock_repo:
        mock_repo.create.return_value = UserDB(
            username="test@mail.com",
            password="123pass",
            role=RolesEnum.USER,
            confirmed=False,
            otp="111234",
            image="https://picsum.photos/id/237/200/300"
        )
        result = user_service.create_new(default_user)
        assert result.confirmed == False
        assert result.otp
        assert result.otp != default_user.otp
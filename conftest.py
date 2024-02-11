import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from app.models.base import Base
from app.schemas.user import User, RolesEnum

TEST_DATABASE__URL = "sqlite:///./test.db "

# @pytest.fixture
# def test_db():
#     engine = create_engine(TEST_DATABASE__URL)
#
#     Base.metadata.create_all(engine)
#
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     db = TestingSessionLocal()
#
#     yield db
#
#     Base.metadata.drop_all(bind=engine)
#     db.close()

@pytest.fixture
def default_user():

    return User(
        username="test@mail.com",
        password="123pass",
        role=RolesEnum.USER,
        confirmed=True,
        otp="111234",
        image="https://picsum.photos/id/237/200/300"
    )

@pytest.fixture
def admin_user():

    return User(
        username="admin@mail.com",
        password="123pass",
        role=RolesEnum.ADMIN,
        confirmed=True,
        otp="111234",
        image="https://picsum.photos/id/237/200/300"
    )

    
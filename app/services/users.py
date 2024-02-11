from repository.user import UserRepo
from schemas.user import User, UserConfirmed
from services.email import send_email


from random import randint

from fastapi import HTTPException



class UserService():
    def __init__(self, db) -> None:
        """
        The __init__ function is the constructor for a class.
        It's called when an instance of the class is created.
        The self parameter refers to the newly created object; it gives 
        the individual instance (not the class) access to methods and properties.
        
        :param self: Represent the instance of the class
        :param db: Create a userrepo object
        :return: None, which is the default return value of any function
        :doc-author: Trelent
        """
        self.repository = UserRepo(db=db)

    def create_new(self, user: User) -> User:
        """
        The create_new function creates a new user and sends an email to the user with a confirmation code.
            Args:
                self (UserService): The UserService object that is calling this function.
                user (User): The User object that will be created in the database.
            Returns:
                new_user (User): A copy of the newly created User from the database.
        
        :param self: Represent the instance of the class
        :param user: User: Pass the user object to the create_new function
        :return: A new user
        :doc-author: Trelent
        """
        user.confirmed = False
        user.otp = str(randint(100000, 999999))
        send_email("Welcome", f"your code is {user.otp}", user.username)
        new_user_from_db = self.repository.create(user)
        new_user = User.from_orm(new_user_from_db)
        return new_user

    def confirmed_user(self, data: UserConfirmed) -> User:
        """
        The confirmed_user function confirms a user by checking the OTP.
            Args:
                data (UserConfirmed): The UserConfirmed object containing the email and OTP.
        
        :param self: Represent the instance of the class
        :param data: UserConfirmed: Pass the data to the function
        :return: A user object
        :doc-author: Trelent
        """
        user = self.get_by_username(data.email)
        if data.otp == user.otp:
            user.confirmed = True
            user = self.repository.update(user)
        return user


    def get_user_for_auth(self, username: str, password: str) -> User:
        """
        The get_user_for_auth function is used to authenticate a user.
            It takes the username and password as arguments, and returns a User object if authentication was successful.
            If authentication fails, it raises an HTTPException with status code 403 (Forbidden).
        
        
        :param self: Represent the instance of a class
        :param username: str: Get the username from the request body
        :param password: str: Check the password of the user
        :return: The user object from the repository
        :doc-author: Trelent
        """
        user = self.repository.get_user_and_check_pass(username, password)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)


    def get_by_username(self, username: str) -> User:
        """
        The get_by_username function is used to retrieve a user by their username.
            If the user does not exist, an HTTPException will be raised with a status code of 403.
        
        :param self: Represent the instance of the class
        :param username: str: Specify the username of the user that we want to get
        :return: An object of type user
        :doc-author: Trelent
        """
        user = self.repository.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)

    def set_image(self, user: User, url: str) -> User:
        """
        The set_image function sets the image of a user.
            Args:
                user (User): The User object to set the image for.
                url (str): The URL of the new image to set for this User.
            Returns:
                A User object with its updated attributes, including its new image URL.
        
        :param self: Represent the instance of a class
        :param user: User: Pass the user object to the function
        :param url: str: Set the image url of the user
        :return: The updated user
        :doc-author: Trelent
        """
        user.image = url
        user_from_db = self.repository.update(user)
        return User.from_orm(user_from_db)



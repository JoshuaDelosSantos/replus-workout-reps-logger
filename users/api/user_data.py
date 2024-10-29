"""
Author: Joshua Delos Santos
Date: 21/10/2024
"""

from django.contrib.auth.models import User
from base.models import Session, Exercise, Line

class UserData:
    """
    A class to handle querying user-related data.
    
    Attributes:
        user (User): The Django User object for which the data is being queried.
        
    Example usage:
        user = UserData(request.user)
        user_details = user_data.get_user_details()
        user_sessions = user_data.get_user_sessions()
        user_exercises = user_data.get_user_exercises()
        user_lines = user_data.get_user_lines()
    """

    def __init__(self, user: User):
        """
        Initializes the UserData instance with the specified user.

        Args:
            user (User): The user whose data will be queried.
        """
        self.user = user


    def get_user_sessions(self):
        """
        Returns all sessions associated with the user.

        Returns:
            QuerySet: A QuerySet containing the user's sessions.
        """
        return Session.objects.filter(user=self.user)


    def get_user_exercises(self):
        """
        Returns all exercises associated with the user through sessions.

        Returns:
            QuerySet: A QuerySet containing the user's exercises.
        """
        return Exercise.objects.filter(session__user=self.user)


    def get_user_lines(self):
        """
        Returns all lines associated with the user's exercises.

        Returns:
            QuerySet: A QuerySet containing the lines related to the user's exercises.
        """
        return Line.objects.filter(exercise__session__user=self.user)

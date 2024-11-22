"""
Author: Joshua Delos Santos
Date: 21/10/2024
"""


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from base.models import Session, Exercise, Line


class AppUser:
    """
    A class to handle querying user-related data.
    
    Attributes:
        user (User): The Django User object for which the data is being queried.
        
    Example usage:
        app_user = AppUser(request.user)
        user_sessions = app_user.get_user_sessions()
        user_exercises = app_user.get_user_exercises()
        user_lines = app_user.get_user_lines()
    """


    def __init__(self, user: User):
        """
        Initializes the AppUser instance with the specified user.

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

    
    def get_exercises_by_session_slug(self, session_slug):
        """
        Returns exercises associated with the user filtered by the selected session slug.

        Args:
            session_slug (str): The slug of the session to filter exercises by.

        Returns:
            QuerySet: A QuerySet containing the exercises for the specified session.
        """
        session = get_object_or_404(Session, slug=session_slug, user=self.user)
        return Exercise.objects.filter(session=session, user=self.user)


    def get_user_lines(self):
        """
        Returns all lines associated with the user's exercises.

        Returns:
            QuerySet: A QuerySet containing the lines related to the user's exercises.
        """
        return Line.objects.filter(exercise__session__user=self.user)


    def get_lines_for_exercise(self, exercise_slug):
        """
        Returns lines associated with the user filtered by the selected exercise slug.

        Args:
            exercise_slug (str): The slug of the exercise to filter lines by.

        Returns:
            QuerySet: A QuerySet containing the lines for the specified exercise.
        """
        exercise = get_object_or_404(Exercise, slug=exercise_slug, session__user=self.user)
        return Line.objects.filter(exercise=exercise)

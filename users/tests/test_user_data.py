"""
Test cases for User data querying.

Author: Joshua Delos Santos
Date: 21/10/2024
"""

from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Session, Exercise, Line
from users.api.user_data import UserData

class UserDataTests(TestCase):
    def setUp(self):
        """
        Set up test data for the UserData class.
        """
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser', password='testpass')

        # Create a session associated with the test user
        self.session = Session.objects.create(name="Test Session", user=self.test_user)

        # Create exercises associated with the session
        self.exercise1 = Exercise.objects.create(name="Test Exercise 1", session=self.session, user=self.test_user)
        self.exercise2 = Exercise.objects.create(name="Test Exercise 2", session=self.session, user=self.test_user)

        # Create lines associated with the exercises
        Line.objects.create(exercise=self.exercise1, weight=100, reps=10, user=self.test_user)
        Line.objects.create(exercise=self.exercise2, weight=150, reps=15, user=self.test_user)

    def test_get_user_sessions(self):
        """
        Test getting sessions associated with the user.
        """
        user_data = UserData(self.test_user)
        sessions = user_data.get_user_sessions()
        self.assertIn(self.session, sessions)

    def test_get_user_exercises(self):
        """
        Test getting exercises associated with the user through sessions.
        """
        user_data = UserData(self.test_user)
        exercises = user_data.get_user_exercises()
        self.assertIn(self.exercise1, exercises)
        self.assertIn(self.exercise2, exercises)

    def test_get_user_lines(self):
        """
        Test getting lines associated with the user's exercises.
        """
        user_data = UserData(self.test_user)
        lines = user_data.get_user_lines()
        self.assertEqual(lines.count(), 2)  # There are 2 lines created
        self.assertTrue(all(line.exercise in [self.exercise1, self.exercise2] for line in lines))

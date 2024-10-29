"""
Test cases for models

Author: Joshua Delos Santos
Date: 07/10/2024
"""

from django.test import TestCase
from .models import Session, Exercise, Line
from django.contrib.auth.models import User


class SessionModelTests(TestCase):
    """
    Test cases for the Session model. 
    """
    def setUp(self):
        """
        Set up a basic Session instance with associated Exercises for testing.
        """
        self.user1 = User.objects.create_user(username="testuser1", password="testpass1")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass2")
        self.session = Session.objects.create(name="Strength Training", user=self.user1)  # Associate session with user1
        self.exercise = Exercise.objects.create(session=self.session, name="Squats", user=self.user1)  # Associate exercise with user1

    def test_exercise_count_in_session(self):
        """
        Test the count of exercises associated with a session.
        """
        self.assertEqual(self.session.exercises.count(), 1)

    def test_user_cannot_access_other_users_session(self):
        """
        Test that user2 cannot access sessions created by user1.
        """
        self.assertFalse(self.user2.sessions.filter(id=self.session.id).exists())


class ExerciseModelTests(TestCase):
    """
    Test cases for the Exercise model.
    """
    def setUp(self):
        """
        Set up a basic Exercise instance with related Line instances for testing.
        """
        self.user1 = User.objects.create_user(username="testuser1", password="testpass1")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass2")
        self.session = Session.objects.create(name="Strength Training", user=self.user1)  # Associate session with user1
        self.exercise = Exercise.objects.create(name="Squats", session=self.session, user=self.user1)  # Associate exercise with user1

    def test_determine_average_reps_with_no_lines(self):
        """
        Test average reps calculation when there are no Line instances.
        """
        average_reps = self.exercise.determine_average_reps()
        self.assertEqual(average_reps, 0)

    def test_determine_average_reps_with_one_line(self):
        """
        Test average reps calculation with a single Line instance.
        """
        Line.objects.create(exercise=self.exercise, weight=100, reps=10, user=self.user1)  # Associate line with user1
        average_reps = self.exercise.determine_average_reps()
        self.assertEqual(average_reps, 10)

    def test_user_cannot_access_other_users_exercise(self):
        """
        Test that user2 cannot access exercises created by user1.
        """
        self.assertFalse(self.user2.exercises.filter(id=self.exercise.id).exists())

    def test_determine_average_reps_with_multiple_lines(self):
        """
        Test average reps calculation with multiple Line instances.
        """
        Line.objects.create(exercise=self.exercise, weight=100, reps=10, user=self.user1)  # Associate line with user1
        Line.objects.create(exercise=self.exercise, weight=150, reps=15, user=self.user1)  # Associate line with user1
        Line.objects.create(exercise=self.exercise, weight=200, reps=20, user=self.user1)  # Associate line with user1

        average_reps = self.exercise.determine_average_reps()
        # Total reps = 10 + 15 + 20 = 45; Number of lines = 3
        self.assertEqual(average_reps, 15)  # 45 / 3 = 15


class LineModelTests(TestCase):
    """
    Testcases for the Line model. 
    """
    def setUp(self):
        """
        Set up a basic Line instance with an associated Exercise for testing.
        """
        self.user1 = User.objects.create_user(username="testuser1", password="testpass1")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass2")
        self.session = Session.objects.create(name="Strength Training", user=self.user1)  # Associate session with user1
        self.exercise = Exercise.objects.create(name="Squats", session=self.session, user=self.user1)  # Associate exercise with user1
        self.line = Line.objects.create(exercise=self.exercise, weight=100.00, reps=10, user=self.user1)  # Associate line with user1

    def test_user_cannot_access_other_users_line(self):
        """
        Test that user2 cannot access lines created by user1.
        """
        self.assertFalse(self.user2.lines.filter(id=self.line.id).exists())

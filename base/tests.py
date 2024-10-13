"""
Test cases for models

Author: Joshua Delos Santos
Date: 07/10/2024
"""

from django.test import TestCase
from .models import Session, Exercise, Line

class SessionModelTests(TestCase):
    def setUp(self):
        """
        Set up a basic Session instance with associated Exercises for testing.
        """
        self.session = Session.objects.create(name="Strength Training")
        self.exercise = Exercise.objects.create(session=self.session, name="Squats")

    def test_exercise_count_in_session(self):
        """
        Test the count of exercises associated with a session.
        """
        self.assertEqual(self.session.exercises.count(), 1)

class ExerciseModelTests(TestCase):
    def setUp(self):
        """
        Set up a basic Exercise instance with related Line instances for testing.
        """
        self.session = Session.objects.create(name="Strength Training")
        self.exercise = Exercise.objects.create(name="Squats", session=self.session)

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
        Line.objects.create(exercise=self.exercise, weight=100, reps=10)
        average_reps = self.exercise.determine_average_reps()
        self.assertEqual(average_reps, 10)

    def test_determine_average_reps_with_multiple_lines(self):
        """
        Test average reps calculation with multiple Line instances.
        """
        Line.objects.create(exercise=self.exercise, weight=100, reps=10)
        Line.objects.create(exercise=self.exercise, weight=150, reps=15)
        Line.objects.create(exercise=self.exercise, weight=200, reps=20)

        average_reps = self.exercise.determine_average_reps()
        # Total reps = 10 + 15 + 20 = 45; Number of lines = 3
        self.assertEqual(average_reps, 15)  # 45 / 3 = 15

class LineModelTests(TestCase):
    def setUp(self):
        """
        Set up a basic Line instance with an associated Exercise for testing.
        """
        self.session = Session.objects.create(name="Strength Training")
        self.exercise = Exercise.objects.create(name="Squats", session=self.session)
        self.line = Line.objects.create(exercise=self.exercise, weight=100.00, reps=10)

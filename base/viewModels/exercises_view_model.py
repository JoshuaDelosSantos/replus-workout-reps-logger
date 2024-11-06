"""
Author:  Joshua Delos Santos
Date:    06/11/2024
"""
    
from base.models import Exercise, Session
from users.api.app_user import AppUser
from base.forms.exercise_form import ExerciseForm
from django.shortcuts import get_object_or_404

class ExerciseViewModel:
    """
    View model for the exercise view.
    
    Example use:
        view_model = ExerciseViewModel(request.user)
        exercises = view_model.get_exercises(session_slug)
    """
    def __init__(self, user):
        """
        Initialize the view model with the authenticated user.
        """
        self.user = user
        
        
    def get_session(self, session_slug):
        """
        Get the session for the given slug.
        
        Returns:
            session: The session if found
        """
        return get_object_or_404(Session, slug=session_slug, user=self.user)
    
    
    def get_exercises(self, session_slug):
        """
        Get the list of exercises for the given session.
        
        Returns:
            exercises: The list of exercises for the session
        """
        user = AppUser(self.user)
        return user.get_exercises_by_session_slug(session_slug)
    
    
    def get_exercise_form(self, data=None):
        """
        Get the form to add a new exercise.
        data = None: GET request
        
        Returns:
            form: The exercise form
        """
        return ExerciseForm(data)
    
    
    def create_exercise(self, form, session):
        """
        Create a new exercise for the authenticated user using the form data.
        
        Returns:
            exercise: The new exercise
        """
        exercise = form.save(commit=False)  # 'commit=False' does not save to the database yet
        exercise.session = session
        exercise.user = self.user
        
        return exercise
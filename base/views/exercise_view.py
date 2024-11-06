"""
Author: Joshua Delos Santos
Date: 31/10/2024
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from base.forms.exercise_form import ExerciseForm
from base.viewModels.exercises_view_model import ExerciseViewModel
from django.core.exceptions import ValidationError

class ExerciseView(View):
    """
    A class-based view for displaying details of an Exercise.
    """
    def setup(self, request, *args, **kwargs):
        """
        Initialize view_model before dispatch.
        Called by Django for each request.
        """
        super().setup(request, *args, **kwargs)
        self.view_model = ExerciseViewModel(request.user)
        
        
    def get(self, request, session_slug):
        """
        Handle GET requests to display the details of exercises in a session.
        """
        context = self._get_context(session_slug)
        
        return render(request, 'base/exercises.html', context)
    
    
    def post(self, request, session_slug):
        """
        Handle POST requests to process the form to add a new exercise.
        """
        session = self.view_model.get_session(session_slug)
        
        return self._handle_add_exercise(request, session)
    
    
    def _get_context(self, session_slug):
        """
        Get the context for the view.
        
        Returns:
            dict: The context for the view.
        """
        exercises = self.view_model.get_exercises(session_slug)
        session = self.view_model.get_session(session_slug)
        form = self.view_model.get_exercise_form()
        
        return {
            'exercises': exercises,
            'session': session,
            'form': form
        }
    
    
    def _handle_add_exercise(self, request, session):
        """
        Handle adding an exercise.
        
        Returns:
            HttpResponse: The response to the request.
        """
        form = self.view_model.get_exercise_form(request.POST)
        
        if form.is_valid():
            try:
                # Using form data, create a new session for user.
                exercise = self.view_model.create_exercise(form, session)
                exercise.save()
                redirect('exercises', session_slug=session.slug)
            except ValidationError as e:
                form.add_error('name', e)
        
        # If form is invalid, display the form with the errors.
        context = {
            'exercises': self.view_model.get_exercises(session.slug),
            'session': session,
            'form': form
        }
        
        return render(request, 'base/exercises.html', context)
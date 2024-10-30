"""
Author: Joshua Delos Santos
Date: 31/10/2024
"""

from django.shortcuts import render, get_object_or_404
from django.views import View
from base.models import Exercise, Session
from users.api.app_user import AppUser
from base.forms.exercise_form import ExerciseForm

class ExerciseView(View):
    """
    A class-based view for displaying details of an Exercise.
    """

    def get(self, request, session_slug):
        """
        Handle GET requests to display the details of exercises in a session.
        """
        user = AppUser(request.user)
        session = get_object_or_404(Session, slug=session_slug, user=request.user)
        exercises = user.get_exercises_by_session_slug(session_slug)
        form = ExerciseForm()
        
        context = {
            'exercises': exercises, 
            'form': form,
            'session': session
        }
        
        return render(request, 'base/exercise.html', context)
    
    def post(self, request, session_slug):
        """
        Handle POST requests to process the form to add a new exercise.
        """
        user = AppUser(request.user)
        session = get_object_or_404(Session, slug=session_slug, user=request.user)
        form = ExerciseForm(request.POST)
        
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user 
            exercise.session = session 
            try:
                exercise.save()
                return redirect('exercise', session_slug=session.slug)
            except ValidationError as e:
                form.add_error(None, e)
                
        context = {
            'session': session, 
            'exercises': exercises, 
            'form': form
            }
        
        exercises = user_data.get_exercises_by_session_slug(session_slug)
        return render(request, 'base/exercise.html', context)
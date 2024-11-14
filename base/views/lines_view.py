"""
Author: Joshua Delos Santos
Date: 31/10/2024
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.exceptions import ValidationError
from base.models import Exercise, Line
from base.forms.line_form import LineForm
from users.api.app_user import AppUser
from base.viewModels.lines_view_model import LinesViewModel

class LinesView(View):
    """
    A class-based view for displaying and adding lines to an exercise.
    """
    def setup(self, request, *args, **kwargs):
        """
        Initialize view_model before dispatch.
        Called by Django for each request.
        """
        super().setup(request, *args, **kwargs)
        self.view_model = LinesViewModel(request.user)
    
    
    def get(self, request, session_slug, exercise_slug):
        """
        Handle GET requests to display the details of lines in an exercise.
        """
        context = self._get_context(session_slug, exercise_slug)
        
        return render(request, 'base/lines.html', context)
    
    
    def post(self, request, session_slug, exercise_slug):
        """
        Handle POST requests to process the form to add a new line.
        """
        user = AppUser(request.user)
        exercise = get_object_or_404(Exercise, slug=exercise_slug, session__slug=session_slug, user=request.user)
        form = LineForm(request.POST)
        
        if form.is_valid():
            line = form.save(commit=False)
            line.user = request.user
            line.exercise = exercise
            try:
                line.save()
                return redirect('lines', session_slug=session_slug, exercise_slug=exercise_slug)
            except ValidationError as e:
                form.add_error(None, e)
        
        lines = user.get_lines_for_exercise(exercise_slug)
        context = {
            'exercise': exercise,
            'lines': lines,
            'form': form
        }
        
        return render(request, 'base/lines.html', context)
    
    
    def _get_context(self, session_slug, exercise_slug):
        """
        Get the context for the view.
        
        Returns:
            dict: The context for the view.
        """
        exercise = self.view_model.get_exercise(session_slug, exercise_slug)
        lines = self.view_model.get_lines(session_slug, exercise_slug)
        form = self.view_model.get_line_form()
        
        return {
            'exercise': exercise,
            'lines': lines,
            'form': form
        }

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

class LinesView(View):
    """
    A class-based view for displaying and adding lines to an exercise.
    """
    def get(self, request, session_slug, exercise_slug):
        """
        Handle GET requests to display the details of lines in an exercise.
        """
        user = AppUser(request.user)
        exercise = get_object_or_404(Exercise, slug=exercise_slug, session__slug=session_slug, user=request.user)
        lines = exercise.lines.all()
        form = LineForm()
        
        context = {
            'exercise': exercise,
            'lines': lines,
            'form': form
        }
        
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
        
        lines = exercise.lines.all()
        context = {
            'exercise': exercise,
            'lines': lines,
            'form': form
        }
        
        return render(request, 'base/lines.html', context)

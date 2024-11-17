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
        if 'delete_line' in request.POST:
            return self._handle_delete_line(request)
        else:
            exercise = self.view_model.get_exercise(session_slug, exercise_slug)
            return self._handle_add_line(request, exercise)
        
    
    
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
        
    
    def _handle_add_line(self, request, exercise):
        """
        Handle adding a line.
        
        Returns:
            HttpResponse: The response to the request.
        """
        form = self.view_model.get_line_form(request.POST)
        session = exercise.session
        
        if form.is_valid():
            try:
                # Using form data, create a new line for user.
                line = self.view_model.create_line(form, exercise)
                line.save()
                return redirect('lines', session_slug=session.slug, exercise_slug=exercise.slug)
            except ValidationError as e:
                form.add_error(None, e)
        
        # If form is invalid, display the form with the errors.
        context = {
            'exercise': exercise,
            'lines': self.view_model.get_lines(session.slug, exercise.slug),
            'form': form
        }
        
        return render(request, 'base/lines.html', context)
    
    
    def _handle_delete_line(self, request):
        """
        Handle deleting a line.
        """
        line_id = request.POST.get('line_id')
        exercise_slug = request.POST.get('exercise_slug')
        session_slug = request.POST.get('session_slug')
        
        self.view_model.delete_line(session_slug, exercise_slug, line_id)
        
        return redirect('lines', session_slug=session_slug, exercise_slug=exercise_slug)
        

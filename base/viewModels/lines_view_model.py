"""
Author:  Joshua Delos Santos
Date:    13/11/2024
"""


from base.models import Exercise, Session
from users.api.app_user import AppUser
from base.forms.line_form import LineForm
from django.shortcuts import get_object_or_404
from base.models import Line


class LinesViewModel:
    """
    View model for the lines view.
    
    Example use:
        view_model = LinesViewModel(request.user)
        lines = view_model.get_lines(session_slug, exercise_slug)
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
    
    
    def get_exercise(self, session_slug, exercise_slug):
        """
        Get the exercise for the given session and exercise slug.
        
        Returns:
            exercise: The exercise if found
        """
        return get_object_or_404(Exercise, slug=exercise_slug, session__slug=session_slug, user=self.user)
    
    
    def get_lines(self, session_slug, exercise_slug):
        """
        Get the list of lines for the given exercise.
        
        Returns:
            lines: The list of lines for the exercise
        """
        user = AppUser(self.user)
        return user.get_lines_for_exercise(exercise_slug)
    
    
    def get_line_form(self, data=None):
        """
        Get the form to add a new line.
        data = None: GET request
        
        Returns:
            form: The line form
        """
        return LineForm(data)
    
    
    def create_line(self, form, exercise):
        """
        Create a new line for the authenticated user using the form data.
        """
        line = form.save(commit=False)
        line.user = self.user
        line.exercise = exercise
        
        return line
    
    
    def delete_line(self, session_slug, exercise_slug, line_id):
        """
        Delete a line for the authenticated user using the line ID.
        
        Args:
            session_slug: Slug of the session
            exercise_slug: Slug of the exercise
            line_id: ID of the line to delete
        """
        exercise = self.get_exercise(session_slug, exercise_slug)
        line = get_object_or_404(Line, 
            id=line_id,
            exercise=exercise,
            user=self.user
        )
        line.delete()
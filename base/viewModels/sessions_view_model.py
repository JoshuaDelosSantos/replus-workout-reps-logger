"""
Author: Joshua Delos Santos
Date: 03/11/2024
"""

from base.models import Session
from users.api.app_user import AppUser
from base.forms.session_form import SessionForm

class SessionsViewModel:
    """
    View model for the sessions view.
    
    Example use:
        view_model = SessionsViewModel(request.user)
        sessions = view_model.get_sessions()
    """
    def __init__(self, user):
        """
        Initialize the view model with the authenticated user.
        """
        self.user = user
    
    
    def get_sessions(self):
        """
        Get the list of sessions for the authenticated user.
        """
        user = AppUser(self.user)
        return user.get_user_sessions()
    
    
    def get_session_form(self, data=None):
        """
        Get the form to add a new session.
        
        data = None: GET request
        """
        return SessionForm(data)
    
    
    def create_session(self, form):
        """
        Create a new session for the authenticated user using the form data.
        
        Returns:
            session: The new session
        """
        session = form.save(commit=False)  # 'commit=False' does not save to the database yet
        session.user = self.user

        return session 
    
    
    def delete_session(self, session_slug):
        """
        Delete a session for the authenticated user using the session slug.
        """
        session = Session.objects.get(slug=session_slug, user=self.user)
        session.delete()
        
        
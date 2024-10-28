"""
Author: Joshua Delos Santos
Date: 28/10/2024
"""

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View

class LogoutView(View):
    """
    Handle user logout.
    """
    def post(self, request):
        """
        Handle POST requests: log out the user and redirect to the home page.
        """
        logout(request)
        return redirect('home')
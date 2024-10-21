"""
Author: Joshua Delos Santos
Date: 02/09/2024
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

class HomeView(View):
    """
    HomeView handles displaying the homepage with the logged-in user's name.

    get(): Renders the homepage and passes the username to the template.
    get_username(): Returns the current user's username if authenticated, otherwise 'Guest'.
    
    The username is provided to 'base/home.html' as 'name' for personalized display.
    """
    def get(self, request):
        """
        Return the homepage.
        """
        name = self.get_username(request)
        return  render(request, 'base/home.html', {'name':name})
    
    def get_username(self, request):
        """
        Return user username.

        Returns:
            String: username if user is authenticated else Guest
        """
        if request.user.is_authenticated:
            return request.user.username
        else:
            return 'Guest'
    
    


def sessions(request):
    """
    Return user session page.
    """
    return render(request, 'session.html')


def statistics(request):
    """
    Return user satatistics page.
    """
    return render(request, 'statistics.html')


def profile(request):
    """
    Return user profile page.
    """
    return render(request, 'profile.html')


def exercise(request):
    """
    Return user exercise page.
    """
    return render(request, 'exercise.html')


def contact(request):
    """
    Return contact page.
    """
    return render(request, 'contact.html')
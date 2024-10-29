"""
Class Models

Author: Joshua Delos Santos
Date: 07/10/2024
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError 

MAX_CHAR_FIELD = 50
MAX_DIGITS = 5
NUMBER_DECIMAL_PLACE = 2

class Session(models.Model):
    name = models.CharField(max_length=MAX_CHAR_FIELD, unique=True)  # Django will raise an IntegrityError when creating a duplicate.
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')  # Link to User
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Override the save method to enforce uniqueness of the session name and 
        automatically set the slug based on the session name.
        """
        if Session.objects.filter(name=self.name, user=self.user).exists() and not self.pk:
            raise ValidationError(f"A session with the name '{self.name}' already exists.")
        
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)
    

class Exercise(models.Model):
    name = models.CharField(max_length=MAX_CHAR_FIELD)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exercises', null=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Override the save method to automatically set the slug based on the exercise name.
        """
        # Automatically generate the slug from the name
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)
    
    def determine_average_reps(self):
        total_reps = sum(line.reps for line in self.lines.all())
        count = self.lines.count()
        return total_reps / count if count > 0 else 0
    
class Line(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='lines')
    weight = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=NUMBER_DECIMAL_PLACE)
    reps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lines') 
    
    def __str__(self):
        return f"{self.weight} for {self.reps} reps at {self.date}"
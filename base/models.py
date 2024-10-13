"""
Class Models

Author: Joshua Delos Santos
Date: 07/10/2024
"""

from django.db import models

MAX_CHAR_FIELD = 50
MAX_DIGITS = 5
NUMBER_DECIMAL_PLACE = 2

class Session(models.Model):
    name = models.CharField(max_length=MAX_CHAR_FIELD)
    
    def __str__(self):
        return self.name
    

class Exercise(models.Model):
    name = models.CharField(max_length=MAX_CHAR_FIELD)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exercises', null=True)
    
    def __str__(self):
        return self.name
    
    def determine_average_reps(self):
        total_reps = sum(line.reps for line in self.lines.all())
        count = self.lines.count()
        return total_reps / count if count > 0 else 0
    
class Line(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='lines')
    weight = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=NUMBER_DECIMAL_PLACE)
    reps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.weight} for {self.reps} reps at {self.date}"
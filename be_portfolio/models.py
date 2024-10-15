from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# portfolio/models.py


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # image_url = models.URLField(max_length=200)
    image_url =models.ImageField(upload_to='project_images/')  # This will upload images to the specified folder
    github_link = models.URLField(max_length=200)
    live_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Add any other fields you need



# Programming sessions for kids
class ProgrammingSession(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)

    def __str__(self):
        return self.title
    
    
    
# Enrollments by parents for their kids
class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(ProgrammingSession, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=100)
    child_age = models.IntegerField()
    enrolled_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.child_name} ({self.child_age} years) in {self.session.title}"
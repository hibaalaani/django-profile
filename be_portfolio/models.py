from django.db import models

# Create your models here.
# portfolio/models.py
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # image_url = models.URLField(max_length=200)
    image_url =models.ImageField(upload_to='project_images/')  # This will upload images to the specified folder
    github_link = models.URLField(max_length=200)
    live_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

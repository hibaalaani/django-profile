from django.contrib import admin

# Register your models here.
from .models import Project
from .models import ProgrammingSession

admin.site.register(Project)


admin.site.register(ProgrammingSession)
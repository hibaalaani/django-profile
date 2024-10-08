from django.http import JsonResponse
from .models import Project
# Create your views here.
def project_list(request):
     projects =Project.objects.all().values()  # Get all projects
     return JsonResponse(list(projects), safe=False)
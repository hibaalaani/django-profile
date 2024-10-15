from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ProgrammingSessionViewSet, EnrollmentViewSet, register, login_view, logout_view, enroll_in_session, payment, dashboard




router = DefaultRouter()
router.register(r'sessions', ProgrammingSessionViewSet)
router.register(r'enrollments', EnrollmentViewSet)



urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
      path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
  
    path('enroll/<int:session_id>/', enroll_in_session, name='enroll'),
    path('payment/<int:session_id>/', payment, name='payment'),
    path('dashboard/', dashboard, name='dashboard'), 
    path('', include(router.urls)),  # Include the URLs from the router (sessions and enrollments)
]

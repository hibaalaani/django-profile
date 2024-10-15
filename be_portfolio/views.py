from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from rest_framework.decorators import api_view
from .models import ProgrammingSession, Enrollment ,Project , CustomUser

import stripe
from django.conf import settings
from rest_framework import viewsets
from .serializers import ProgrammingSessionSerializer, EnrollmentSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
# from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def project_list(request):
     projects =Project.objects.all().values()  # Get all projects
     return JsonResponse(list(projects), safe=False)




# Viewset for Programming Sessions
class ProgrammingSessionViewSet(viewsets.ModelViewSet):
    queryset = ProgrammingSession.objects.all()
    serializer_class = ProgrammingSessionSerializer

# Viewset for Enrollments
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']  # You can include other fields if needed
        extra_kwargs = {
            'password': {'write_only': True}  # This ensures the password is write-only
        }
    def create(self, validated_data):
        # This ensures that the password is hashed when saved
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# User registration API
# User registration API
# @csrf_exempt
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User login API
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# User logout API
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


# Enroll in a session API
@api_view(['POST'])
def enroll_in_session(request, session_id):
    session = get_object_or_404(ProgrammingSession, id=session_id)
    child_name = request.data.get('child_name')
    child_age = request.data.get('child_age')
    enrollment = Enrollment.objects.create(user=request.user, session=session, child_name=child_name, child_age=child_age)
    enrollment.save()
    return Response({"message": f"Enrollment successful for {child_name}"}, status=status.HTTP_201_CREATED)


# Stripe payment API
@api_view(['POST'])
def payment(request, session_id):
    session = get_object_or_404(ProgrammingSession, id=session_id)
    token = request.data.get('stripeToken')
    
    if token:
        try:
            stripe.Charge.create(
                amount=int(session.cost * 100),  # Amount in cents
                currency="eur",
                description=f"Payment for {session.title}",
                source=token,
            )
            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Stripe token missing"}, status=status.HTTP_400_BAD_REQUEST)


# Dashboard to show user enrollments
@api_view(['GET'])
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
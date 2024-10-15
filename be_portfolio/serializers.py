# serializers.py
from rest_framework import serializers
from .models import CustomUser, ProgrammingSession, Enrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class ProgrammingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingSession
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

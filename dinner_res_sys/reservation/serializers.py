import re
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Check if the username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        
        # Check if the email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email']=user.email
        
        return token


class OperationalHoursSerializer(serializers.Serializer):
    open_time = serializers.TimeField()
    close_time = serializers.TimeField()

class RestaurantSerializer(serializers.ModelSerializer):
    operational_hours = OperationalHoursSerializer(write_only=True)
    
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'address', 'phone_no', 'website', 'operational_hours']

    def create(self, validated_data):
        operational_hours = validated_data.pop('operational_hours')
        open_time = operational_hours['open_time']
        close_time = operational_hours['close_time']
        restaurant = Restaurant.objects.create(
            open_time=open_time,
            close_time=close_time,
            **validated_data
        )
        return restaurant
    

class BookedSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedSlot
        fields = ['res_start_time', 'res_end_time']

class RestaurantViewSerializer(serializers.ModelSerializer):
    booked_slots = BookedSlotSerializer(many=True, read_only=True, source='booked_restaurant')

    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'address', 'website', 'phone_no', 'open_time', 'close_time', 'slug', 'booked_slots']
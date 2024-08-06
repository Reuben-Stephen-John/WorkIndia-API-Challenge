from django.shortcuts import render
from django.contrib.auth import authenticate
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .serializers import *
from .models import *

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def get_routes(request):
    routes = [
        '/signup/',
        '/login/',
        '/logout/',
        '/dining-place/create/',
        '/dining-place?name={search_query}',
        '/dining-place/availability',
        '/dining-place/book',

    ]
    return Response(routes)


class UserSignUpAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            Customer.objects.create(customer=user)
            customer = Customer.objects.get(customer=user)
            # Generate JWT tokens upon successful registration
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    'status':"Account successfully created",
                    'status_code':'200',
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_id': customer.slug, 
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            customer = Customer.objects.get(customer=user)
            return Response({
                'status': 'Login successful',
                'status_code': 200,
                'user_id': customer.slug,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        else:
            return Response({
                'status': 'Incorrect username/password provided. Please retry',
                'status_code': 401
            }, status=status.HTTP_401_UNAUTHORIZED)
        

class CreateDiningPlaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        customer = Customer.objects.get(customer=user)

        if customer.profile_type != "Admin":
            return Response({
                "message": "Permission denied. Only admins can add dining places.",
                "status_code": 403
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            restaurant = serializer.save()
            return Response({
                "message": f"{restaurant.restaurant_name} added successfully",
                "place_id": restaurant.slug,
                "status_code": 200
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiningPlaceListView(generics.ListAPIView):
    serializer_class = DiningPlaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('name', '')
        return Restaurant.objects.filter(restaurant_name__icontains=search_query)


class CheckAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        place_id = request.query_params.get('place_id')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        try:
            restaurant = Restaurant.objects.get(slug=place_id)
        except Restaurant.DoesNotExist:
            return Response({'status': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        # Convert times from string to datetime
        start_time = parse_datetime(start_time)
        end_time = parse_datetime(end_time)

        # Check if the place is available
        conflicting_slots = BookedSlot.objects.filter(
            booked_restaurant=restaurant,
            res_start_time__lt=end_time,
            res_end_time__gt=start_time
        ).order_by('res_start_time')

        if not conflicting_slots.exists():
            response_data = {
                'place_id': restaurant.id,
                'name': restaurant.restaurant_name,
                'phone_no': str(restaurant.phone_no),
                'available': True,
                'next_available_slot': None
            }
        else:
            # Find the next available slot
            last_end_time = conflicting_slots.last().res_end_time
            next_available_slot = last_end_time.isoformat()

            response_data = {
                'place_id': restaurant.id,
                'name': restaurant.restaurant_name,
                'phone_no': restaurant.phone_no,
                'available': False,
                'next_available_slot': next_available_slot
            }

        return Response(response_data)


class MakeBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        place_id = request.data.get('place_id')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        user = request.user

        try:
            restaurant = Restaurant.objects.get(slug=place_id)
        except Restaurant.DoesNotExist:
            return Response({'status': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        start_time = parse_datetime(start_time)
        end_time = parse_datetime(end_time)

        if BookedSlot.objects.filter(
            booked_restaurant=restaurant,
            res_start_time__lt=end_time,
            res_end_time__gt=start_time
        ).exists():
            return Response({'status': 'Slot is not available at this moment, please try some other place',
                             'status_code':400}, status=status.HTTP_400_BAD_REQUEST)

        # Create the booking
        booked_slot = BookedSlot.objects.create(
            booked_customer=user.customer,
            booked_restaurant=restaurant,
            res_start_time=start_time,
            res_end_time=end_time
        )

        return Response({
            'status': 'Slot Booked Successfully',
            'status_code':200,
            'booking_id': booked_slot.slug
        }, status=status.HTTP_200_OK)
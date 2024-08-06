# myapp/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('',get_routes,name="get_routes"),

    path('signup/', UserSignUpAPIView.as_view(), name='user_signup'),
    path('login/', UserLoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dining-place/create/', CreateDiningPlaceAPIView.as_view(), name='create_dining_place'),
    path('dining-place', DiningPlaceListView.as_view(), name='dining-place-list'),
    path('dining-place/availability', CheckAvailabilityView.as_view(), name='check-availability'),
    path('dining-place/book', MakeBookingView.as_view(), name='make-booking'),
]

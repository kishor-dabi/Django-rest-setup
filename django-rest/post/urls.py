from django.urls import path, include
from django.conf.urls import url
from .views import UserAddressView, CreateUserAddressView, UserAddressAPIView

urlpatterns = [
    path('user-address', UserAddressView.as_view()),
    path('new-address', CreateUserAddressView.as_view()),
    path('user-address/<int:pk>', UserAddressAPIView.as_view()),
]


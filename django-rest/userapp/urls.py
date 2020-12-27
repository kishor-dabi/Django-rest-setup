from django.urls import path, include
from django.conf.urls import url
from userapp.views import UserRegistrationView, UserLoginView, UserProfileView, UserProfileUpdate, CarViewSet, PartViewSet, PartListView, PartCreateView, CarListView, CarCreateView
from userapp.all_views.reset_and_change_password_view import ChangePasswordView

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^login', UserLoginView.as_view()),
    url(r'^profile', UserProfileView.as_view()),
    path('update-profile/<int:pk>', UserProfileUpdate.as_view()),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('part/<int:pk>', PartViewSet.as_view(), name='part'),
    path('add-part', PartCreateView.as_view(), name='part_add'),
    path('parts', PartListView.as_view(), name='parts'),
    path('cars', CarListView.as_view(), name='car'),
    path('car/<int:pk>', CarViewSet.as_view(), name='car'),
    path('add-car', CarCreateView.as_view(), name='car_add'),

    # path('permission/', include('django_rest.userrole.urls')),
    url(r'^address/', include('post.urls')),
]
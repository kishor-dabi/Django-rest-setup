# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, PartSerializer, CarSerializer
from .models import UserRole, Car, Part
# from django_rest.userrole.serializer import UserRoleSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from userapp.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileUpdateSerializer, CarSerializerWithPart
from rest_framework.generics import RetrieveAPIView

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from userapp.models import User
from .auth import JWTAuthentication
from post.serializers import UserAddressSerializer
from rest_framework import filters

#import for login

from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
# end



class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=request.data)

        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        response = None
        status_code = 0

        if user is None:
            print('no user found')
            response = {"message": 'Invalid email or password.'}
        else:
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
                response = {
                    'success': 'True',
                    'status_code': status.HTTP_200_OK,
                    'message': 'User logged in  successfully',
                    'token': jwt_token,
                    "email": user.email
                }
            except User.DoesNotExist:
                print('error')
                response = {"message": 'Invalid email or password'}

        status_code = status.HTTP_200_OK
        print(response)
        return Response(response, status=status_code)

class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()

    def get(self, request):
        try:
            # ur = UserSerializer(data=request.user)
            # print(ur, ur.is_valid())
            print(request.user, request.user.id )
            user_profile = User.objects.get(id=request.user.id)
            status_code = status.HTTP_200_OK
            print(user_profile)
            # userser = UserSerializer(data=user_profile)
            print(user_profile, '{===========================')
            serializer = None
            if user_profile.role is not None:
                roledata = UserRole.objects.get(pk=user_profile.role.id)
                # serializer = UserRoleSerializer(roledata)
            # print(userser.is_valid() )
            # ad = UserAddressSerializer(user_profile.user_location)
            # print(ad)
            # userroleser = UserRoleSerializer(data=user_profile.role)
            # print(userroleser.is_valid())
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    'email': user_profile.email,
                    'role': serializer,
                    # 'profile':user_profile.data
                    },
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

    def get_queryset(self):
        queryset = User.objects.all()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class UserProfileUpdate(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()
    serializer_class = UserProfileUpdateSerializer
    def put(self, request, pk, format=None):
        # pk = request.user
        if 'id' not in request.data:
            request.data['id'] = pk
        print(request.data, "request.data.id")
        instance = self.get_object()
        print(instance)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("serializer", status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'success': 'true',
            'status code': status.HTTP_200_OK,
            'message': 'User update successfully',
            'data': [{
                # 'first_name': user_profile.first_name,
                # 'last_name': user_profile.last_name,
                # 'phone_number': user_profile.phone_number,
                # 'age': user_profile.age,
                # 'gender': user_profile.gender,
            }]
        }
        return Response(response, status=status.HTTP_200_OK)


class PartViewSet(RetrieveUpdateDestroyAPIView):
    """
    List all workers, or create a new worker.
    """
    permission_classes = (IsAuthenticated,)

    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartListView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Part.objects.all()
    serializer_class = PartSerializer


class CarViewSet(RetrieveUpdateDestroyAPIView):
    """
    List all workkers, or create a new worker.
    """
    permission_classes = (IsAuthenticated,)

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['release_date']
    def patch(self, request, *args, **kwargs):
        print(request.data)
        pk = request.user.id
        if 'id' not in request.data:
            request.data['id'] = pk
        print(request.data, "request.data.id")
        instance = self.get_object()
        print(instance,"-------------------------")
        # instance.parts.clear()

        for item in request.data['parts']:
            print(item, "====================")
            partobj = Part.objects.filter(id=item['id'])
            print(partobj.values())
            instance.parts.add(partobj[0] )


        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CarListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Car.objects.all()
    serializer_class = CarSerializerWithPart
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['release_date']

class CarCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['release_date']


from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from userapp.auth import JWTAuthentication
from .serializers import UserAddressSerializer, UserAddressCreateSerializer
from .models import UserAddress
# Create your views here.
class UserAddressView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()
    queryset = UserAddress.objects.all()

    def get(self, request):
        try:
            queryset = self.get_queryset()
            print(queryset)
            serializer = UserAddressSerializer(queryset, many=True)
            status_code = status.HTTP_200_OK
            # print(user_profile.role, '{===========================', user_profile.role.id)
            # roledata = UserRole.objects.get(pk=user_profile.role.id)
            # serializer = UserRoleSerializer(roledata)
            # print(serializer,serializer.data )
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': serializer.data
                # [{
                    # 'first_name': user_profile.first_name,
                    # 'last_name': user_profile.last_name,
                    # 'phone_number': user_profile.phone_number,
                    # 'age': user_profile.age,
                    # 'gender': user_profile.gender,
                    # 'role': serializer.data
                    # }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Address does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

class CreateUserAddressView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()

    def create(self, request):
        print(request.data)
        serializer = UserAddressCreateSerializer(data=request.data)
        print(serializer.is_valid(raise_exception=True), '-----------------')
        serializer.is_valid(raise_exception=True)
        # user_profile = UserProfile.objects.get(user=request.user)
        try:
            sdata = serializer.save()
            data = UserAddressSerializer(sdata)
            print(data.data)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User Address created successfully',
                'data': data.data
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User Address not created',
                'error': e
            }
        return Response(response, status=status_code)

class UserAddressAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()
    queryset = UserAddress.objects.all()

    def get(self, request, pk, format=None):
        print(pk, "--------------------------")
        try:
            UAddress = UserAddress.objects.get(pk=pk)
            print(UAddress)
            serializer = UserAddressSerializer(UAddress)
            print( serializer, "=======================================after save")

            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Address fetched successfully',
                'data': serializer.data
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Address not fetch',
                'data': str(e)
            }
        return Response(response, status=status_code)
    def put(self, request, pk, format=None):
        print(pk, "--------------------------")
        try:
            print(request.data, "request.data.id")
            instance = self.get_object()
            print(instance)
            serializer = UserAddressCreateSerializer(instance, data=request.data)

            if serializer.is_valid():
                aa = serializer.save()
                # serializer = UserAddressSerializer(UAddress)
                print(aa)
                adata = UserAddressSerializer(aa)
                print( aa, adata.data, '---------------------------------after save')
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'true',
                    'status code': status_code,
                    'message': 'Address Updated successfully',
                    'data': adata.data
                }
                return Response(response, status=status_code)

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'Address not fetch',
                'data': str(e)
            }
            return Response(response, status=status_code)

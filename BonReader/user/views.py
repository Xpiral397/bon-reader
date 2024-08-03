from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User

class CustomActivationView(APIView):
    @swagger_auto_schema(
        operation_description="Activate user account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='Activation code'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            },
            required=['code', 'email']
        ),
        responses={
            200: openapi.Response('Account activated successfully'),
            400: openapi.Response('Invalid activation code or email'),
        }
    )
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        email = request.data.get('email')

        if not code or not email:
            return Response({'error': 'Code and email are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email, activation_code=code)
        
        user.is_active = True
        user.activation_code = ''  # Clear the activation code
        user.save()
        return Response({'status': 'Account activated successfully'}, status=status.HTTP_200_OK)

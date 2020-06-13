from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from UsersApp.models import Buyer
from django.contrib.auth import authenticate
from .serializers import EmailAuthenticationSerializer
import datetime
import jws
from datetime import datetime, timedelta, date
from rest_framework import status

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_jwt.settings import api_settings


def generate_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

# Create your views here.
class BuyerLogin(ObtainAuthToken):
    def get_response(self, serializer):
        if serializer.is_valid() and serializer.validated_data['user']:
            user = serializer.validated_data['user']
            if(user):
                try:
                    buyer = Buyer.objects.get(user=user)
                    print("Printing the buyer")
                    print(buyer.__dict__)
                    if(buyer.confirmation_status):
                        expiry = date.today() + timedelta(days=10)
                        token = generate_jwt_token(user)
                        print("Token : ", token)
                        return Response({
                            'token' : token,
                            'username' : user.username,
                            'email' : user.email,
                            'name' : f"{user.first_name} {user.last_name}",
                            'contact' : buyer.contact,
                            "success": True
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'success' : False,
                            'error' : "Please validate the email"
                        })
                except Buyer.DoesNotExist:
                    return Response(
                        {"result": "error", "message": "Only registered students are allowed to login"},
                        status=status.HTTP_401_UNAUTHORIZED)
                return Response({"result": "error",
                                 "message": "please provide required fields username/email , password"},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response({"result": serializer.errors, "message": "invalid credentials"},
                        status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        # stream = BytesIO(request.body)
        # data = dict(JSONParser().parse(stream))
        data = request.data
        # Checking if the user is validating using email or username
        serializer = EmailAuthenticationSerializer(data=request.data, context={'request': request})
        return self.get_response(serializer)

        return Response({'error': "Invalid credentials", "result" : "unsuccessful"},
                        status=status.HTTP_401_UNAUTHORIZED)

# def create_jwt(request):

#         """
#         the above token need to be saved in database, and a one-to-one
#         relation should exist with the username/user_pk
#         """

#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         expiry = datetime.date.today() + timedelta(days=50)
#         token = jws.sign({'username': user.username, 'expiry':expiry}, 'seKre8',  algorithm='HS256')

#     return HttpResponse(token)
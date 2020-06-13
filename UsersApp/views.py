from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Buyer

from django.core.mail import EmailMessage

from rest_framework.decorators import api_view, authentication_classes,permission_classes
from django.db.models import F, Value

from django.contrib.auth.models import User
from .serializer import BuyerSerializer, BuyerUpdateSerializer
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Create your views here.
@api_view(['GET'])
def index(request):
    return Response({"Result" : "Success"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def auth(request, token):
    user = Token.objects.get(key = token).user
    buyer = Buyer.objects.get(user = user)
    buyer.confirmation_status = True
    buyer.save()    
    return Response({"Result" : "Success"}, status=status.HTTP_200_OK)


def email_exists(email, username = None):
    userObj = User.objects.filter(email = email.lower())
    if(username):
        userObj = userObj.exclude(username = username.lower())
    return userObj.exists()
    
def arrange_buyer_data(validated_data):
    buyer_data_list = ['first_name', 'last_name', 'username', 'email', 'password']
    buyer_data = {}
    for key, value in validated_data.items():
        if(key in buyer_data_list):
            buyer_data[key] = value
    
    buyer_data['email'] = buyer_data.get('email').lower()
    buyer_data['username'] = buyer_data.get('username').lower()
    validated_data["user"] = buyer_data
    return validated_data

class BuyerListView(APIView):
    def get(self, request):
        buyers = Buyer.objects.values('contact').annotate(
            username = F('user__username'),
            first_name = F('user__first_name'),
            last_name = F('user__last_name'),
            email = F('user__email')
            )
        return Response({'buyers' : buyers}, status = status.HTTP_200_OK)

    def post(self, request):
        print("Apple PAple")

        data = arrange_buyer_data(request.data)
        buyer_serializer = BuyerSerializer(data = data)
        error = None
        buyer = None
        if buyer_serializer.is_valid():

            if(not email_exists(data.get('user').get('email'))):
                buyer, error  = buyer_serializer.create(validated_data =buyer_serializer.validated_data)
                if(buyer):
                    # send_mail(subject, message, from_email, to_list, fail_silently=True)
                    subject = "Email Verification for  Gift Cards Nepal"
                    message = "<b>Thank you for sining in to the Account</b> \n Please click on the link below to validate your account"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [buyer.user.email, settings.EMAIL_HOST_USER]
                    token = Token.objects.create(user=buyer.user)
                    verification_url = "http://localhost:8000/user/auth/" + str(token) + "/"
                    sendSignupConfirmationEmail(to_list, buyer.user.first_name, buyer.user.last_name, verification_url)
                    return Response ({"success" : True, "data" : buyer_serializer.data}, status = status.HTTP_200_OK)
            else:
                error = {"user":{"email": ["Email address already exists"]}}
        else:
            error = buyer_serializer.errors
        return Response ({"success":False, "error" : error}, status= status.HTTP_200_OK)

class BuyerDetailView(APIView):
    def get(self, request, username):
        buyer_data = Buyer.objects.get(user__username = username)
        buyer_serializer = BuyerSerializer(buyer_data)
        return Response({"buyer" : buyer_serializer.data}, status=status.HTTP_200_OK)


    def put(self, request, username):
        updated_value = request.data
        print("username", username)
        buyer = Buyer.objects.get(user__username = username)
        print("Printing the updated value")
        print(updated_value)
        error = None
        try:
            print("inside try... .. .. .. .. . .. .. .. .. .. .. .. .. .. .. .......... . .. ")
            print(not email_exists(updated_value.get('user').get('email'), updated_value.get('user').get('username')))
            if(not email_exists(updated_value.get('user').get('email'), updated_value.get('user').get('username'))):
                print("Update here")
                buyer_serializer = BuyerUpdateSerializer(instance = buyer, data=updated_value)
                if(buyer_serializer.is_valid()):    
                    print("Updating the buyers info")
                    print(updated_value)
                    buyer_serializer.update(buyer,updated_value)
                    print(buyer_serializer.data)     
                    return Response({
                        'result' : 'success',
                        'buyer' : buyer_serializer.data}, status=status.HTTP_200_OK)
                error = buyer_serializer.errors
            else:
                error = {"user":{"email":"email address already exists"}}
        except KeyError as e:
            error = e
        
        return Response({'error' : error})

    def delete(self, request, username):
        buyer = Buyer.objects.get(username = username)
        buyer.delete()
        return Response({"result" : "succcess"}, status = status.HTTP_200_OK)




def sendSignupConfirmationEmail(email_list, first_name, last_name, verification_link):
    gmail_user = "prashishmSingh@gmail.com"
    gmail_pwd = "Applemac122"
    TO_LIST = email_list
    SUBJECT = "Giftcards Nepal Email Confirmation and verification"
    TEXT = f"""
    Thank you {first_name} {last_name} for joining Giftcards nepal
    Please click on the link for email verification
    <a href = "{verification_link}"> Verufy Email </a>
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % TO_LIST,
            'From: %s' % gmail_user,
            'Subject: %s' % SUBJECT,
            '', TEXT])

    server.sendmail(gmail_user, TO_LIST, BODY)
    server.quit()

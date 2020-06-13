from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import django.core.exceptions as ex

class EmailAuthenticationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        print("Printing the attribute")
        print(attrs)
        email = attrs.get('email')
        password = attrs.get('password')

        print(email)
        print(password)
        attrs['user'] = None

        if email and password:
            user = get_object_or_404(User, email=email.lower())

            username = user.username
            print("here")
            user = authenticate(username=username, password=password)

            print("Authenticaing the user")
            print(user)
            if user:
                attrs['user'] = user
        else:
            msg = _("Error!! Email or password is not provided")
            raise ex.ValidationError(msg)

        return attrs
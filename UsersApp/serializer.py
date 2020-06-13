from rest_framework import serializers
from .models import Buyer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}
        

class BuyerUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    def update(self, instance, validated_data):
            user_data = validated_data.pop('user')
            
            print(instance.__dict__)
            user_instance = instance.user
            user = update_user(user_instance, user_data)
            instance.contact = validated_data.get('contact')
            user.save()
            instance.save()
            return instance
    class Meta:
        model= Buyer
        fields = '__all__'
            
class BuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = create_buyer_user(user_data)
        error = None
        buyer = None
        if user:
            user.save()
            validated_data['user'] = user
            buyer = Buyer(**validated_data)
            buyer.save()
        else:
            error = "Invalid User information "
        return buyer, error

    class Meta:
        model= Buyer
        fields = '__all__'

def update_user(user_instance, user_data):
    user_instance.first_name = user_data.get('first_name')
    user_instance.last_name = user_data.get('last_name')
    return user_instance


def arrange_buyer_data(validated_data):
    buyer_data_list = ['first_name', 'last_name', 'username', 'email', 'password']
    buyer_data = {}
    for key, value in validated_data.items():
        if(key in buyer_data_list):
            buyer_data[key] = validated_data[key]
            del buyer_data[key]
    return buyer_data_list, buyer_data


def create_buyer_user(validated_data):
    print("Printing the validate data")
    print(type(validated_data))
    print(validated_data)
    user = User.objects.create(**validated_data)
    "Printing the password"
    print(user.password)
    user.set_password(user.password)
    return user
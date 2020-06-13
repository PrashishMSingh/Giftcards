from rest_framework import serializers
from .models import Card, Category, Transaction, Gateway, Booking, Category
from django.contrib.auth.models import User

class CardSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def create(self, validated_data):
        card = Card(**validated_data)
        card.save()
        return card

    def update(self, instance, validated_data):
        instance.dollar_price = validated_data.get('dollar_price')
        instance.selling_price = validated_data.get('selling_price')
        instance.save()
        return instance

    class Meta:
        model= Card
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all())
    gateway = serializers.PrimaryKeyRelatedField(queryset=Gateway.objects.all())

    def create(self, validated_data):
        transaction = Transaction(**validated_data)
        transaction.save()
        return transaction

    class Meta:
        model= Card
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        booking = Booking(**validated_data)
        booking.save()
        return booking
    
    class Meta:
        model = Booking
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.dollar_price = validated_data.get('dollar_price', instance.dollar_price)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Card, Transaction, Category, Gateway, Booking
from .serializers import CardSerializer, BookingSerializer, CategorySerializer
from django.db.models import Value as V, F, Count
from django.db.models.functions import Concat, Cast, Coalesce
from django.db.models import Count, Case, When, IntegerField


from django.core.paginator import Paginator
# from rest_framework.pagination import PaginationSerializer

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from django.db.models import IntegerField
import requests as req
from django.conf import settings
from rest_framework.settings import api_settings

from .pagination import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def getCategories(request):
    categories =  Category.objects.all()
    category_serializer = CategorySerializer(categories, many = True)
    return Response({"categories" : category_serializer.data})


class PaginationAPIView(APIView):
    '''
    APIView with pagination
    '''
    pagination_class= StandardResultsSetPagination

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

# Create your views here.
@api_view(['POST'])
def index(request):
    
    print(request.data)
    return Response({"result" : "success"}, status=status.HTTP_200_OK)


class BookingDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    @staticmethod
    def get(request, booking_id):
        try:
            booking = Booking.objects.get(id = booking_id)
            booking_serializer = BookingSerializer(booking)
            return Response({"booking" : booking_serializer.data})
        except Booking.DoesNotExist:
            return Response({"result" : "failed", "Error": "Object doest not exist"})
    
    @staticmethod
    def put(request, booking_id):
        booking_data = request.data
        user_id = request.user.id
        category = Category.objects.get(category = booking_data.get('category'))
        booking_data["user"] = user_id
        booking_data["category"] = category.id
        booking_serializer = BookingSerializer(data = booking_data)
        if(booking_serializer.is_valid()):
            booking = Booking.objects.get(id = booking_id)
            booking_serializer.update(instance = booking, validated_data = booking_serializer.validated_data)
            return Response({"result": "Success", "data" : booking_serializer.data})
        return Response({"error" : booking_serializer.errors})

    @staticmethod
    def delete(request, booking_id):
        booking = Booking.objects.get(id= booking_id)
        booking.delete()
        return Response({"result" : "success"})

class BookingListView(APIView):
    permission_classes = (IsAuthenticated,)
    @staticmethod
    def get(request):
        print("Printing the username")
        print(request.user.username)
        bookings = Booking.objects\
            .filter(user__username = request.user.username)\
            .values('id', 'dollar_price', 'date')\
            .annotate(category = F('category__category'))
        return Response(bookings, status = status.HTTP_200_OK)

    @staticmethod
    def post(request):
        data = request.data
        data["user"] = request.user.id
        print("Printing the data")
        print(data)
        booking_serializer = BookingSerializer(data = data)
        error = ""
        if(booking_serializer.is_valid()):
            booking = booking_serializer.create(booking_serializer.validated_data)
            if(booking):
                print("Booking comleted")
                return Response(booking_serializer.data, status = status.HTTP_200_OK)
        else:
            error = booking_serializer.errors
        return Response({"Error" : error})
        

class TransactionListView(APIView):
    permission_classes = (IsAuthenticated,)
    @staticmethod
    def get(request):
        transaction = Transaction.objects\
        .filter(user__username = request.user.username)\
        .values('date')\
        .annotate(
            category = F("card__category__category"),
            dollar_price = F("card__dollar_price"),
            paid_amount = F("card__selling_price") ,  
            p_id = F('card__pinCode'),
            gateway = F('gateway__gateway')         
            )
        return Response(transaction, status = status.HTTP_200_OK)


class CardListView(APIView):
    def get(self, request, category = None, page_no = 1):
        cards_category = ["Google", "Amazon", "Itunes"]
        cards = Card.objects
        if category in cards_category:
            cards = Card.objects.filter(category__category = category)
        \
        cards = cards\
                .values('selling_price', 'dollar_price')\
                .annotate(
                    category =F('category__category'),
                    category_id = F('category__id'),
                    stock = Count(
                        Case(
                            When(status = False, then= F('category__category')),
                            output_field = IntegerField()
                            )
                        ) 
                    )
        try:
            paginator = Paginator(list(cards), 8)
            page = paginator.page(page_no)
        except :
            return Response({"data" : {}, "page_no" : page_no, "page_range" : list(paginator.page_range)})    
            
        return Response({"data" : page.object_list, "page_no" : page_no, "page_range" : list(paginator.page_range)})
        
@api_view(['POST'])
def request_esewa_payment(request):
    url ="https://uat.esewa.com.np/epay/main"
    d = {'amt': 100,
        'pdc': 0,
        'psc': 10,
        'txAmt': 0,
        'tAmt': 110,
        'pid':'ee2c3ca1-696b-4cc5-a6be-2c40d929d453',
        'scd':'epay_payment',
        'su':'http://merchant.com.np/page/esewa_payment_success?q=su',
        'fu':'http://merchant.com.np/page/esewa_payment_failed?q=fu'}
    resp = req.post(url, d)
    print(resp)
    return Response({"response" : resp})

@api_view(['GET'])
def payment_verification(request):
    url ="https://tokentest.com.np/inquiry/12123122"
    # d = {
    #     'amt': 100,
    #     'scd': 'epay_payment',
    #     'rid': '000AE01',
    #     'pid':'ee2c3ca1-696b-4cc5-a6be-2c40d929d453',
    # }
    headers = {
        "content-type" : "Application/Json",
        "username" : "test5@esewa.com",
        "password" : "test12"
    }
    resp = req.get(url, headers = headers)
    print(resp.text)
    return Response({"response" : resp})


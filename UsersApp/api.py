from .views import index
from django.urls import path
from .views import BuyerListView, BuyerDetailView,auth

urlpatterns = [
    path('', index),
    path('auth/<str:token>/', auth),
    path('buyer/', BuyerListView.as_view()),
    path('buyer/<str:username>/', BuyerDetailView.as_view())
]


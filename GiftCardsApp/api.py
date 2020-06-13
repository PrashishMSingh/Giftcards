from .views import index
from django.urls import path
from .views import CardListView, request_esewa_payment, TransactionListView, payment_verification, \
BookingListView, getCategories, BookingDetailView


urlpatterns = [
    path('', index),
    path('cards/<str:category>/<int:page_no>/', CardListView.as_view()),
    path('transactions/', TransactionListView.as_view()),
    path('bookings/', BookingListView.as_view()),
    path('bookings/<int:booking_id>/', BookingDetailView.as_view()),
    path('esewa_payment/', payment_verification),
    path('categories/', getCategories)
]


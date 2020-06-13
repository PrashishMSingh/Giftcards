from django.urls import path
from .views import BuyerLogin


from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', csrf_exempt(BuyerLogin.as_view()))

]

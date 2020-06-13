from django.contrib import admin
from .models import Category, Gateway, Card, Transaction, Booking

# Register your models here.
admin.site.register(Category)
admin.site.register(Gateway)
admin.site.register(Card)
admin.site.register(Booking)
admin.site.register(Transaction)

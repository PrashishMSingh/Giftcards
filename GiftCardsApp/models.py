from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class Gateway(models.Model):
    gateway = models.CharField(max_length = 100)

    def __str__(self):
        return self.gateway

class Card(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dollar_price = models.IntegerField()
    selling_price = models.IntegerField()
    pinCode = models.CharField(max_length= 200, unique = True)
    status = models.BooleanField()

    def __str__(self):
        return self.category.category + " - " + str(self.dollar_price) + '$'

class Transaction(models.Model):
    card = models.ForeignKey(Card, on_delete=  models.PROTECT)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    date = models.DateField(auto_now_add=True, blank=False)
    gateway = models.ForeignKey(Gateway, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.date) + ' - ' + self.gateway.gateway + ' - ' + self.user.username + ' - ' + self.card.category.category + ' - ' + str(self.card.dollar_price)



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dollar_price = models.IntegerField()
    date = models.DateField(auto_now_add=True, blank=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " - " + self.category.category + " - " + str(self.dollar_price)


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length = 10, unique = True)
    confirmation_status= models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
from django.db import models
from userapp.models import User

# Create your models here.

class UserAddress(models.Model):
    location = models.CharField(max_length=100)
    user_location = models.ManyToManyField(User)#, through='UserLocation'

    class Meta:
        """
        to set table name in database
        """
        db_table = "user_address"
#
# class UserLocation(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     location = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
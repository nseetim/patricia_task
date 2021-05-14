from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class AppUser(AbstractUser):
    name = models.CharField(max_length=250)
    api_key = models.CharField(max_length=400)
    web_hook_url = models.CharField(max_length=400)

class Transaction(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='transactions')
    transaction_reference = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    client_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=5)

# Model for Keeping the Request Logs
class RequestLogs(models.Model):
    endpoint = models.CharField(max_length=100, null=True) # The url the user requested
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True) # User that made request, if authenticated
    response_code = models.PositiveSmallIntegerField() # Response status code
    method = models.CharField(max_length=10, null=True)  # Request method
    remote_address = models.CharField(max_length=20, null=True) # IP address of user
    exec_time = models.IntegerField(null=True) # Time taken to create the response
    date = models.DateTimeField(auto_now=True) # Date and time of request
    body_response = models.TextField() # Response data
    body_request = models.TextField() # Request data

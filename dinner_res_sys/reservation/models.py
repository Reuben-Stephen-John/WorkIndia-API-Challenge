import uuid
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .choices import *


# Create your models here.
class Customer(models.Model):
    customer=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_type=models.CharField(max_length=100, choices=STATUS_CHOICES, default="User")
    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(Customer, self).save(*args, **kwargs)

class Restaurant(models.Model):
    restaurant_name=models.CharField(max_length = 100)
    address=models.CharField(max_length=300)
    website=models.URLField(max_length=200, blank=True, null=True)
    phone_no = PhoneNumberField( null=True)
    open_time=models.TimeField()
    close_time=models.TimeField()
    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(Restaurant, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.restaurant_name)+' -> '+str(self.website)+' -> '+str(self.open_time)+' -> '+str(self.close_time)

class BookedSlot(models.Model):
    booked_customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='booked_customer')
    booked_restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='booked_restaurant')
    res_start_time=models.DateTimeField()
    res_end_time=models.DateTimeField()
    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(BookedSlot, self).save(*args, **kwargs)


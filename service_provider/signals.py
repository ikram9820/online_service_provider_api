from turtle import pos
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from . import models

@receiver(post_save,sender = get_user_model())
def create_location_for_new_user(sender,**kwargs):
    if kwargs['created']:
        models.Location.objects.create(user = kwargs['instance'])
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField()
    contact = models.PositiveBigIntegerField(null=True)
    

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering =['username']

    

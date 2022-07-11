from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()

class Location(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'location', primary_key= True)

    def __str__(self) -> str:
        return f'{self.x}, {self.y}'
        
    class Meta:
        ordering = ['user__username']


class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']

class ServiceProvider(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    status = models.BooleanField(default=True)
    rate_per_hour = models.DecimalField(max_digits=6,decimal_places=2)
    avr_rating = models.SmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    description = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    radius = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='sp')

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        ordering = ['user__username']


class Order(models.Model):
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='order')
    sp = models.ForeignKey(ServiceProvider , on_delete= models.CASCADE, related_name='request')

    def __str__(self) -> str:
        return f'{self.user.username} order {self.sp.username}'
    
    class Meta:
        ordering = ['ordered_at']

class Review(models.Model):
    rate = models.SmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='review_user')
    sp = models.ForeignKey(ServiceProvider , on_delete= models.CASCADE, related_name='sp_review')


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_chat')
    sp = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sp_chat')

    class Meta:
        unique_together = [['user','sp']]

class Message(models.Model):
    texted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='message')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='send_text')

    def __str__(self) -> str:
        return self.author.username
        
    class Meta:
        ordering = ['texted_at']
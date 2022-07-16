from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()

class Location(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'location', primary_key= True)

    def __str__(self) -> str:
        return f'{self.user.username}\'s {self.x}, {self.y}'
        
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
    rate_per_hour = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    avr_rating = models.FloatField(default =0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    description = models.TextField(default="")    
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='sp',default=1)


    def save(self,*args,**kwargs) -> None:
        Range.objects.get_or_create(sp=self)
        super(ServiceProvider,self).save(*args,**kwargs)

    

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        ordering = ['user__username']

class Range(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    radius = models.IntegerField(default=0)
    address = models.CharField(max_length=500,null=True)
    sp = models.OneToOneField(ServiceProvider,on_delete=models.CASCADE,related_name='range',primary_key=True)
    
    
    def __str__(self) -> str:
        return f'{self.sp.user.username} range is {self.radius/1000} km'

    class Meta:
        ordering = ['radius']
    

class Order(models.Model):
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='order')
    sp = models.ForeignKey(ServiceProvider , on_delete= models.CASCADE, related_name='request')

    def __str__(self) -> str:
        return f'{self.user.username} order {self.sp.user.username}'
    
    class Meta:
        ordering = ['ordered_at']

class Review(models.Model):
    rate = models.SmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='review_user')
    order = models.OneToOneField(Order , on_delete= models.CASCADE, related_name='order_review',primary_key=True)


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_chat')
    sp = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE,related_name='sp_chat')

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
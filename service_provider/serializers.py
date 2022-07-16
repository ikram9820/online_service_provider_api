from rest_framework import serializers
from . import models

class ServiceProviderSerialzer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    
    class Meta:
        model = models.ServiceProvider
        fields = ['user_id','rate_per_hour','description','category']

 
class LocationSerialzer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Location
        fields = ['user_id','x','y']

class RangeSerialzer(serializers.ModelSerializer):
    
    sp_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Range
        fields = ['sp_id','x','y','radius','address']

 
class OrderSerializer(serializers.ModelSerializer):
    ordered_at = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    sp_id = serializers.IntegerField(read_only = True)
    is_accepted = serializers.BooleanField(read_only = True)
    is_completed = serializers.BooleanField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','ordered_at','sp_id','user_id','is_accepted','is_completed']

    def create(self, validated_data):
        user_id = self.context['user_id']
        sp_id = self.context['sp_id']
        if not user_id:
            raise serializers.ValidationError("please login first!")
        (order,created) = models.Order.objects.get_or_create(user_id = user_id ,sp_id=sp_id,is_completed = False,**validated_data)
        return order


class AcceptOrderSerializer(serializers.ModelSerializer):
    ordered_at = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    sp_id = serializers.IntegerField(read_only = True)
    is_completed = serializers.BooleanField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','ordered_at','sp_id','user_id','is_accepted','is_completed']


class CompleteOrderSerializer(serializers.ModelSerializer):
    ordered_at = serializers.DateTimeField(read_only = True)
    user_id = serializers.IntegerField(read_only = True)
    sp_id = serializers.IntegerField(read_only = True)
    is_accepted = serializers.BooleanField(read_only = True)
    class Meta:
        model = models.Order
        fields = ['id','ordered_at','sp_id','user_id','is_accepted','is_completed']

class ReviewSerializer(serializers.ModelSerializer):

    order_id = serializers.IntegerField(read_only= True)
    user_id = serializers.IntegerField(read_only= True)

    class Meta:
        model = models.Review
        fields = ['rate', 'review', 'user_id','order_id']

    def create(self, validated_data):
        order_id = self.context['order_id']
        user_id = self.context['user_id']
        return models.Review.objects.create(order_id=order_id,user_id= user_id, **validated_data)


class ChatSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    sp_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Chat 
        fields = ['id','sp_id','user_id']
    
    def create(self, validated_data):
        sp_id = self.context['sp_id']
        user_id = self.context['user_id']
        (chat,created )= models.Chat.objects.get_or_create(sp_id=sp_id,user_id= user_id, **validated_data)
        return chat


class ChatMessagesSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(read_only = True)
    author_id = serializers.IntegerField(read_only = True)
    texted_at = serializers.DateTimeField(read_only = True)
    class Meta:
        model = models.Message
        fields = ['chat_id','author_id','texted_at','text']

    def create(self, validated_data):
        chat_id = self.context['chat_id']
        user_id = self.context['user_id']
        return models.Message.objects.create(chat_id=chat_id,author_id= user_id, **validated_data)

from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.decorators import action ,api_view
from rest_framework.response import Response
from rest_framework import permissions

from . import serializers
from . import models

@api_view(['GET','PUT','HEAD'])
def my_location(request ):
    try:
        loc = models.Location.objects.get(user_id= request.user.id) 
    except ObjectDoesNotExist:
        return Response("Now you have to be  login first , in future it  will be taken from gps",status= status.HTTP_405_METHOD_NOT_ALLOWED)
    if request.method == 'GET':
        serializer = serializers.LocationSerialzer(loc)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = serializers.LocationSerialzer(loc, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

def range(x1,y1,x2,y2):
    x = (x2-x1)**2
    y = (y2-y1)**2
    res = x+y
    return res**(1/2)

class ServiceProviderViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ServiceProviderSerialzer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        my_loc = models.Location.objects.get(user_id = self.request.user.id)
        sp_ids_in_range = models.Range.objects.filter(radius__gte = range(my_loc.x,my_loc.y,F('x'),F('y'))).values_list('sp_id')
        return models.ServiceProvider.objects.filter(user_id__in =sp_ids_in_range,status = True)

    @action(detail= True )
    def reviews(self,request,pk):
        order_ids = models.Order.objects.filter(sp_id = pk,is_completed = True).values_list('pk')
        reviews = models.Review.objects.filter(pk__in = order_ids)   
        rate =0
        rate = [ review.rate for review in reviews] 
        print(sum(rate),reviews.count())
        rate = sum(rate) /reviews.count()   
        models.ServiceProvider.objects.filter(pk = pk ).update(avr_rating = rate)
        serializer = serializers.ReviewSerializer(reviews,many = True)
        return Response(serializer.data)

    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def my_range(self, request):
        try:
            sp = models.ServiceProvider.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            return Response("you don't have this type of account",status= status.HTTP_405_METHOD_NOT_ALLOWED)
        range = models.Range.objects.get(sp_id=sp.pk)

        if request.method == 'GET':
            serializer = serializers.RangeSerialzer(range)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.RangeSerialzer( range, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        (sp,created)= models.ServiceProvider.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = serializers.ServiceProviderSerialzer(sp)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.ServiceProviderSerialzer(sp, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return models.Order.objects.filter(sp_id = self.kwargs['service_pk'])

    def get_serializer_context(self):
        return {'sp_id':self.kwargs['service_pk'],\
                "user_id":self.request.user.id if self.request.user.is_authenticated else None}

    @action(methods=['GET','PATCH'],detail=True,)
    def accept_order(self,request,service_pk,pk):
        order = models.Order.objects.get(pk = pk)
        print(service_pk)
        if request.method == 'GET':
            serializer = serializers.AcceptOrderSerializer(order)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            sps_order = models.Order.objects.filter(sp_id = service_pk,is_accepted = True , is_completed = False)
            if sps_order:
                return Response ("you can't accept multiple order",status=status.HTTP_405_METHOD_NOT_ALLOWED)
            serializer = serializers.AcceptOrderSerializer(order,data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
    
            set_sp_status(service_pk)
            return Response(serializer.data)

    @action(methods=['GET','PATCH'],detail=True,)
    def complete_order(self,request,service_pk,pk):
        order = models.Order.objects.get(pk = pk)
        print(order)
        if request.method == 'GET':
            serializer = serializers.CompleteOrderSerializer(order)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            if not order.is_accepted:
                return Response("order is not accepted you cann't check complete ")
            serializer = serializers.CompleteOrderSerializer(order,data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            
            set_sp_status(service_pk)

            return Response(serializer.data)

def set_sp_status(service_pk):
    sps_order = models.Order.objects.filter(sp_id = service_pk,is_accepted = True , is_completed = False)
    if sps_order:
        models.ServiceProvider.objects.filter(pk = service_pk).update(status =False)
    else:
        models.ServiceProvider.objects.filter(pk = service_pk).update(status =True)

class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def create(self, request,order_pk, *args, **kwargs):
        order = models.Order.objects.get(pk = order_pk)
        if not order.is_completed:
            return Response('order is not completed. you can review only completed order.',status= status.HTTP_405_METHOD_NOT_ALLOWED)
        if order.order_review:
            return Response('you cann\'t  give multiple review to order.' , status= status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        return models.Review.objects.filter(order_id=self.kwargs['order_pk'])

    def get_serializer_context(self):
        return {'user_id' :self.request.user.id,'order_id': self.kwargs['order_pk']}


class ChatViewSet(ModelViewSet):
    serializer_class = serializers.ChatSerializer
    
    def get_queryset(self):
        return models.Chat.objects.filter(sp_id = self.kwargs['service_pk'],user_id = self.request.user.id)

    def get_serializer_context(self):
        return {'user_id' :self.request.user.id,'sp_id': self.kwargs['service_pk']}


class ChatMessagesViewSet(ModelViewSet):
    serializer_class = serializers.ChatMessagesSerializer

    def get_queryset(self):
        return models.Message.objects.filter(chat_id = self.kwargs['chat_pk'])

    def get_serializer_context(self):
        return {'user_id' :self.request.user.id,'chat_id': self.kwargs['chat_pk']}



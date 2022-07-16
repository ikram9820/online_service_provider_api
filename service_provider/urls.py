from cgitb import lookup
from email.mime import base
from rest_framework_nested import routers
from django.urls import path
from . import views


router = routers.DefaultRouter()

router.register('services', views.ServiceProviderViewSet, basename='services')
services_router = routers.NestedDefaultRouter(router,'services',lookup = 'service')
services_router.register('orders',views.OrderViewSet,basename='service-orders')
services_router.register('chats',views.ChatViewSet,basename='service-chats')

order_router = routers.NestedDefaultRouter(services_router,'orders',lookup = 'order')
order_router.register('review',views.ReviewViewSet,basename='oreder-review')

chat_router = routers.NestedDefaultRouter(services_router,'chats',lookup = 'chat')
chat_router.register('messages',views.ChatMessagesViewSet,basename = 'chat-messages')

urlpatterns =[
path('my_location/',views.my_location),
] + router.urls + services_router.urls +order_router.urls +chat_router.urls
from rest_framework import permissions
from . import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

    

class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

        
    def has_object_permission(self, request, view, obj):
        
        if self.has_permission(request,view):
            return bool(obj.sp_id == request.user.id) or bool(obj.user_id == request.user.id) #tested just for order
        return False

class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request,view):
        order_pk = view.kwargs['order_pk']
        if bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        ):
            try:
                models.Order.objects.get(pk = order_pk , user_id =request.user.id)
                return True
            except ObjectDoesNotExist:
                return False
        return False

        
    def has_object_permission(self, request, view, obj):
        
        if self.has_permission(request,view):
            return bool(obj.user.id == request.user.id)  
        return False


class ChatPermission(permissions.BasePermission):
            
    def has_object_permission(self, request, view, obj):       
        user_id = request.user.id
        return bool(obj.user.id == user_id or obj.sp.pk == user_id)  

class MessagePermmision(permissions.BasePermission):
     
    def has_permission(self, request, view):
        user = request.user
        if bool(
            user and user.is_authenticated
        ):  
            chat_pk = int(view.kwargs['chat_pk'])
            chat = models.Chat.objects.get(pk = chat_pk)
            return bool(chat.sp.pk == user.id or chat.user.id == user.id)


    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            request.method in permissions.SAFE_METHODS or
            user and user.is_authenticated and bool(obj.author_id == user.id)
        )



class OrderUserPermission(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return bool(obj.user_id == request.user.id) #tested just for order
        return False

class OrderSpPermission(permissions.BasePermission):

        
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return bool(obj.sp_id == request.user.id) #tested just for order
        return False



# class IsAuthenticatedServiceProvider(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return super().has_permission(request, view)
    
#     def has_object_permission(self, request, view, obj):
#         return super().has_object_permission(request, view, obj)




# class IsAuthenticatedServiceProvider(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if bool(request.user and request.user.is_authenticated):
#             try:
#                 models.ServiceProvider.objects.get(pk=request.user.id)
#                 return True
#             except ObjectDoesNotExist:
#                 return False
#         return False
        
#     def has_object_permission(self, request, view, obj):
#         return super().has_object_permission(request, view, obj)


# class IsAuthenticatedServiceProvider(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if bool(request.user and request.user.is_authenticated):
#             try:
#                 models.ServiceProvider.objects.get(pk=request.user.id)
#                 return True
#             except ObjectDoesNotExist:
#                 return False
#         return False
        
#     def has_object_permission(self, request, view, obj):
#         if bool(request.user and request.user.is_authenticated):
#             return bool(obj.sp_id == request.user.id) 
#         return False

# class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
#     def __init__(self) -> None:
#         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

# class ViewCustomerHistoryPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.has_perm('store.view_history')
from django.contrib import admin
from . import models

class UserLocationInline(admin.TabularInline):
    model = models.Location

class ServiceRangeInline(admin.TabularInline):
    model = models.Range

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_editable = ['name']
    list_per_page = 10
    search_fields = ['name','id']


class ServiceOrderInline(admin.TabularInline):
    model = models.Order

@admin.register(models.ServiceProvider)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceRangeInline,ServiceOrderInline]
    list_display = ['user_id','user','status','avr_rating','category',]
    search_fields = ['user__username','category__name']
    list_editable = ['user','category']
    list_per_page = 10




class ChatMessagesInline(admin.TabularInline):
    model = models.Message

class OrderReviewInline(admin.TabularInline):
    model = models.Review



@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sp','user']
    inlines = [ChatMessagesInline]
    list_per_page = 10

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['author','author_id','chat','text','texted_at',]
    search_fields = ['text']
    list_editable = ['text']
    list_per_page = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderReviewInline]
    list_display = ['user','sp','is_accepted','is_completed','ordered_at',]
    list_editable = ['is_accepted','is_completed']
    list_per_page = 10
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','order','rate','review']
    list_editable = ['rate','review']
    list_per_page = 10


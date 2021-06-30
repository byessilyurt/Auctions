from django.contrib import admin
from .models import User,Profile,Category,Item,BidItem,CommentItem, WatchList
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(BidItem)
admin.site.register(CommentItem)
admin.site.register(WatchList)
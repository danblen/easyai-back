from django.contrib import admin

from .models import UserImage, Image, User
# Register your models here.
admin.site.register(UserImage)
admin.site.register(Image)
admin.site.register(User)

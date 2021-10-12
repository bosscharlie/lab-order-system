from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy


# Register your models here.

class RoomConfig(admin.ModelAdmin):
    list_display = ('caption', 'capacity')
    list_filter = ('capacity',)
    search_fields = ('caption', 'capacity')


class BookConfig(admin.ModelAdmin):
    list_display = ('user', 'room', 'date', 'time_id')
    list_filter = ('user', 'room', 'date', 'time_id')
    search_fields = ('user', 'room', 'date', 'time_id')


class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('last_login', 'is_staff', 'date_joined', 'is_active')
    search_fields = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        #(gettext_lazy('用户信息'), {'fields': ('username', 'email', 'tel', 'avatar')}),
        (gettext_lazy('用户权限'), {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(models.Room, RoomConfig)
admin.site.register(models.UserInfo, UserProfileAdmin)
admin.site.register(models.Book, BookConfig)

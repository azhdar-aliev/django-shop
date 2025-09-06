from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User


# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    inlines = [CartTabAdmin, OrderTabulareAdmin]





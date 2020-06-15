from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email_confirmed", "confirmation_code", "first_name", "last_name", "bio", "email", "role")
    


admin.site.register(User, UserAdmin)

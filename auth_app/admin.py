from django.contrib import admin

from auth_app.models import *


class AccountAdmin(admin.ModelAdmin):
    model = Account
    fieldsets = [
        ('Name', {'fields': ['email']}),
        ('Account information',
         {'fields': ['is_superuser', 'is_staff', 'last_login', 'is_active'], 'classes': ('collapse',)}),
    ]


admin.site.register(Account, AccountAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            'Employee Information',
            {
                'fields': (
                    'department',
                    'designation',
                    'profile_image',
                    'salary',
                )
            },
        ),
    )

    list_display = (
        'username',
        'first_name',
        'department',
        'designation',
        'salary',
        'is_staff',
    )
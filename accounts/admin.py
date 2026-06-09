from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'department',
        'designation',
        'joining_date',
        'location',
        'phone',
    )

    search_fields = (
        'user__username',
        'department',
        'designation',
        'location',
    )

    list_filter = (
        'department',
        'designation',
        'location',
    )
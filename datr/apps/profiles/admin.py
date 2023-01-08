from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Profile Data',
            {
                'fields': (
                    'bio',
                    'profile_pic'
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)

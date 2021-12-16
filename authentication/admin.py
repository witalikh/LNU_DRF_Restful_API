from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    """ Class for django-admin page """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email', 'first_name', 'last_name', )
    list_filter = ('email', )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (None, {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)

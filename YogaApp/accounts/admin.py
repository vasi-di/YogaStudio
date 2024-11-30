from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm
from .models import Profile
from django.contrib.auth import get_user_model


UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    model = UserModel
    add_form = RegistrationForm

    list_display = ('pk', 'email', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name')
    ordering = ('user', 'first_name')




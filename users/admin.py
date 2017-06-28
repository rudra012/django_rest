from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('email',)
    actions_on_bottom = True

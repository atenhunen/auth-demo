from django.contrib import admin
from auth_demo.models.user import User

admin.autodiscover()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


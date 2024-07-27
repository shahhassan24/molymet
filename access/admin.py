from django.contrib import admin
from access.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	pass

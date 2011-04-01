from django.contrib import admin
from georegistry.accounts.models import UserProfile, Permission


admin.site.register(UserProfile)
admin.site.register(Permission)
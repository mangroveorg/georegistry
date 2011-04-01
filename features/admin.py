from django.contrib import admin
from models import FacilityType


class FacilityTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','slug')

admin.site.register(FacilityType, FacilityTypeAdmin)
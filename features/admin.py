from django.contrib import admin
from models import ClassifierTypes, ClassifierCategories
from models import ClassifierSubcategories, Classifiers, Since


class ClassifierTypesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','slug')

class ClassifierCategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','slug')
    
class ClassifierSubcategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','slug')

admin.site.register(ClassifierTypes, ClassifierTypesAdmin)
admin.site.register(ClassifierCategories,ClassifierCategoriesAdmin)
admin.site.register(ClassifierSubcategories,ClassifierSubcategoriesAdmin)
admin.site.register(Classifiers)
admin.site.register(Since)
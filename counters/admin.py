from django.contrib import admin

from models import AllFeaturesCounter, CountryFeaturesCounter

from models import ClassifierCategoryFeaturesCounter, ClassifierTypeFeaturesCounter


admin.site.register(AllFeaturesCounter)
admin.site.register(ClassifierCategoryFeaturesCounter)
admin.site.register(ClassifierTypeFeaturesCounter)
admin.site.register(CountryFeaturesCounter)


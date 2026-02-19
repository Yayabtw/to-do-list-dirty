from django.contrib import admin

from .models import FranceConnectProfile, Series

admin.site.register(Series)
admin.site.register(FranceConnectProfile)

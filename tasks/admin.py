from django.contrib import admin

from .models import FranceConnectProfile, GoogleProfile, Series

admin.site.register(Series)
admin.site.register(FranceConnectProfile)
admin.site.register(GoogleProfile)

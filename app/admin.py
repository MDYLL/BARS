from django.contrib import admin

from .models import Recruit, Sith, Planet,ShadowHand

# Register your models here.
admin.site.register(Recruit)
admin.site.register(Sith)
admin.site.register(ShadowHand)
admin.site.register(Planet)

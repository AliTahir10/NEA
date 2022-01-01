from django.contrib import admin

# Register your models here.

from .models import *
# all models made need to be registered so that they can be viewed in the admin page
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Request)
admin.site.register(Block)
admin.site.register(Tag)
admin.site.register(Producttag)

from django.contrib import admin
from .models import customer, product, repair

# Register your models here.

admin.site.register(customer)
admin.site.register(product)
admin.site.register(repair)
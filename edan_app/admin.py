from django.contrib import admin
from . models import LoginTable,guest_table

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(guest_table)
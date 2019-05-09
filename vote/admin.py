from django.contrib import admin
from .models import *

for model in DB_MODELS:
    admin.site.register(model)

# Register your models here.

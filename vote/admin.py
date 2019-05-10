from django.contrib import admin
from .models import *


# Register your models here.
class VoteModelAdmin(admin.ModelAdmin):
    list_filter = ('user', 'headline')
    list_display = ('headline', 'user', 'timestamp')


admin.site.register(Headline)
admin.site.register(Vote, VoteModelAdmin)

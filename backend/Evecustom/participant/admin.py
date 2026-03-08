from django.contrib import admin
from participant.models import createteam, jointeam
admin.site.register(createteam)
admin.site.register(jointeam)
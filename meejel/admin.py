from django.contrib import admin, messages
from .models import *

admin.site.site_header = 'Meejel Administration'
admin.site.index_title = 'MEEJEL'
admin.site.site_title = 'Meejel Admin'


class AssessmentAdmin(admin.ModelAdmin):
    model = Assessment
    list_display = ('id', 'name', 'owner')
    list_filter = ('name', 'owner')


admin.site.register(Assessment, AssessmentAdmin)

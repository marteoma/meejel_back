from django.contrib import admin, messages
from .models import *

admin.site.site_header = 'Meejel Administration'
admin.site.index_title = 'MEEJEL'
admin.site.site_title = 'Meejel Admin'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'name')
    list_filter = ('name', )


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    model = Instrument
    list_display = ('name', 'owner', 'level', 'associated_concepts', 'difficulty', 'time', 'winner_selection',
                    'category', 'purpose_teaching', 'purpose_reinforce', 'purpose_check', 'purpose_social',)
    list_filter = ('name', 'owner', 'category', 'difficulty')


@admin.register(Principle)
class PrincipleAdmin(admin.ModelAdmin):
    model = Principle
    list_display = ('principle', 'grade', )
    list_filter = ('principle', 'grade')


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    model = Component
    list_display = ('instrument', 'description', 'component_type')
    list_filter = ('instrument', )


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    model = Evidence
    list_display = ('principle', 'component')

# main/admin.py
from django.contrib import admin
from .models import SummerProgram, Course, ProgramSection # ProgramSection'ı import et

@admin.register(ProgramSection)
class ProgramSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'order')
    list_filter = ('program',)
    list_editable = ('order',) # Admin panelinden sıralamayı kolayca değiştirmek için

admin.site.register(SummerProgram)
admin.site.register(Course)
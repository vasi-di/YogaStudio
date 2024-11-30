from django.contrib import admin
from .models import YogaClass, Instructor


@admin.register(YogaClass)
class YogaClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule', 'level', 'instructor')
    list_filter = ('level', 'schedule')
    search_fields = ('name', 'level')
    ordering = ('schedule',)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio', 'experience_years', 'specializations')
    list_filter = ('experience_years', 'specializations')
    search_fields = ('name',)
    ordering = ('name',)



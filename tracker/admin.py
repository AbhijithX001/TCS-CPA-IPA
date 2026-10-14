"""
Admin configuration for TCS CPA/IPA Tracker models.
"""
from django.contrib import admin
from .models import Subject, StudyDay, Task, CodingPractice, MistakeLog


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'section_type', 'marks', 'questions_count', 'time_info']
    list_filter = ['section_type']
    search_fields = ['code', 'name']


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ['subject', 'title', 'is_completed', 'order', 'resource_url', 'resource_label', 'notes']


@admin.register(StudyDay)
class StudyDayAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'focus_summary']
    inlines = [TaskInline]
    search_fields = ['title', 'focus_summary']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'day', 'is_completed', 'order']
    list_filter = ['is_completed', 'subject', 'day']
    search_fields = ['title', 'notes']
    list_editable = ['is_completed', 'order']


@admin.register(CodingPractice)
class CodingPracticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'time_taken_mins', 'day']
    list_filter = ['category', 'status']
    search_fields = ['title', 'key_edge_cases']
    list_editable = ['status']


@admin.register(MistakeLog)
class MistakeLogAdmin(admin.ModelAdmin):
    list_display = ['topic_or_question', 'subject', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'subject']
    search_fields = ['topic_or_question', 'what_went_wrong', 'correct_concept_or_fix']
    list_editable = ['is_resolved']

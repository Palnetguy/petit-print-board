from django.contrib import admin
from .models import PrintRequest


@admin.register(PrintRequest)
class PrintRequestAdmin(admin.ModelAdmin):
    list_display = ['filename', 'teacher', 'status', 'deadline', 'copies', 'created_at']
    list_filter = ['status', 'created_at', 'deadline']
    search_fields = ['filename', 'teacher__username', 'teacher__first_name', 'teacher__last_name']
    readonly_fields = ['created_at', 'updated_at', 'printed_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('teacher', 'file', 'filename', 'deadline', 'copies', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at', 'printed_at')
        }),
    )

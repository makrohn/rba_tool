from django.contrib import admin

# Register your models here.
from .models import System, Role, Access

class AccessInline(admin.TabularInline):
    model = Access
    extra = 3

class RoleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['role_name']}),
    ]
#    list_display = ('role_name')
    inlines = [AccessInline]
#    list_filter = ['role_name']
#    search_fields = ['associated_system']


admin.site.register(Role, RoleAdmin)
admin.site.register(System)

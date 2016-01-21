from django.contrib import admin
from .models import Service, Role, Access, Team

class AccessInline(admin.TabularInline):
    """Set up access fields for admin views"""
    model = Access
    extra = 3

class RoleAdmin(admin.ModelAdmin):
    """Edit role name, select membership, show service access levels in admin view"""
    fieldsets = [
        (None,               {'fields': ['role_name']}),
        (None,               {'fields': ['membership']}),
    ]
    inlines = [AccessInline]

class ServiceAdmin(admin.ModelAdmin):
    """Edit server name, show role access levels in admin view"""
    fieldsets = [
        (None,               {'fields': ['service_name']}),
        (None,               {'fields': ['responsible_team']}),
    ]
    inlines = [AccessInline]

admin.site.register(Role, RoleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Team)

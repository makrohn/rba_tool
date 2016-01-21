from django.contrib import admin

# Register your models here.
from .models import Service, Role, Access, Team

class AccessInline(admin.TabularInline):
    model = Access
    extra = 3

class RoleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['role_name']}),
        (None,               {'fields': ['membership']}),
    ]
    inlines = [AccessInline]

class ServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['service_name']}),
        (None,               {'fields': ['responsible_team']}),
    ]
    inlines = [AccessInline]

admin.site.register(Role, RoleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Team)

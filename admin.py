from django.contrib import admin

# Register your models here.
from .models import Service, Role, Access

class AccessInline(admin.TabularInline):
    model = Access
    extra = 3

class RoleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['role_name']}),
        (None,               {'fields': ['memberships']}),
    ]
    inlines = [AccessInline]

class ServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['service_name']}),
    ]
    inlines = [AccessInline]

admin.site.register(Role, RoleAdmin)
admin.site.register(Service, ServiceAdmin)

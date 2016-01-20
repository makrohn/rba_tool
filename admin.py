from django.contrib import admin

# Register your models here.
from .models import System, Role, Access

class AccessInline(admin.TabularInline):
    model = Access
    extra = 3

class RoleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['role_name']}),
        (None,               {'fields': ['memberships']}),
    ]
    inlines = [AccessInline]

class SystemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['system_name']}),
    ]
    inlines = [AccessInline]

admin.site.register(Role, RoleAdmin)
admin.site.register(System, SystemAdmin)

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

class System(models.Model):
    system_name = models.CharField(max_length=200, unique=True)
#    access_level = models.CharField(max_length=200)
    def __str__(self):
        return self.system_name

class Role(models.Model):
    role_name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.role_name
    memberships = models.ForeignKey('self', null=True, blank=True)
    access_levels = models.CharField(max_length=2000, default='{}')
    def get_access(self):
        access_dict = eval(self.access_levels)
        for system in System.objects.all():
            if system.system_name not in access_dict:
                access_dict[system.system_name] = ''
        return access_dict
    def save_access(self, some_dict):
        self.access_levels = repr(some_dict)

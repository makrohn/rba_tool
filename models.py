import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

class System(models.Model):
    system_name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.system_name

class Role(models.Model):
    role_name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.role_name
    memberships = models.ForeignKey('self', null=True, blank=True)

class Access(models.Model):
    access_level = models.CharField(max_length=400, null=True, blank=True)
    associated_role = models.ForeignKey(Role)
    associated_system = models.ForeignKey(System)
    def __str__(self):
        return self.access_level

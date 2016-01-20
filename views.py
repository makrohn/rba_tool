from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Role, Service, Access, Team
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

def index(request):
    role_list = Role.objects.order_by('role_name')
    template = loader.get_template('rba/index.html')
    context = {
        'role_list': role_list,
    }
    return HttpResponse(template.render(context, request))

def getAccess(role):
    role_access={}
    for item in Access.objects.filter(associated_role=role):
        role_access[item.associated_service.service_name] = item.access_level
    return role_access

def accessResults(request, role_id):
    role = Role.objects.get(pk=role_id)
    total_access = getAccess(role)
    for membership in role.memberships.all():
        total_access.update(getAccess(membership))
    response = "A %s ought to have" + repr(total_access)
    return HttpResponse(response % role.role_name)

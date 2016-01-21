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
        role_access[item.associated_service.service_name] = str(item.access_level).split(",")
    return role_access

def accessResults(request, role_id):
    role = Role.objects.get(pk=role_id)
    total_access = getAccess(role)
    while role.membership:
        privileges=(getAccess(role.membership))
        for privilege in privileges:
            if privilege in total_access:
                for priv in privileges[privilege]:
                    total_access[privilege].append(priv)
            else:
                total_access[privilege] = privileges[privilege]
        role = role.membership
    response = "A %s ought to have" + repr(total_access)
    template = loader.get_template('rba/access.html')
    context = {
        'access': total_access,
        'role': role.role_name
    }
    return HttpResponse(template.render(context, request))

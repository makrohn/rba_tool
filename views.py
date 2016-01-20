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

def accessDisplay(request, total_access):
    template = loader.get_template('rba/access.html')
    context = {
        'access_list': total_access,
    }
    return HttpResponse(template.render(context, request))

def calc_access(request, role_id):
    role = Role.objects.get(role_name=role_id)
    total_access={}
    for item in Access.objects.filter(associated_role=role):
        total_access[item.associated_service] = item.access_level
    return HttpResonseRedirect(reverse('accessDisplay',args=(total_access)))

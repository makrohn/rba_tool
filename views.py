from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Role, Service, Access
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

def index(request):
    role_list = Role.objects.order_by('role_name')
    template = loader.get_template('rba/index.html')
    context = {
        'role_list': role_list,
    }
    return HttpResponse(template.render(context, request))


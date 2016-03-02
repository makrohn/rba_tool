"""Where the magic happens to figure out what a new hire needs"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Role, Service, Access, Team
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template.defaulttags import register


def index(request):
    """Generate list of clickable links to find access"""
    role_list = Role.objects.order_by('role_name')
    template = loader.get_template('rba/index.html')
    context = {
        'role_list': role_list,
    }
    return HttpResponse(template.render(context, request))


def get_access(role):
    """Compile all accesses for a given role"""
    role_access = {}
    for item in Access.objects.filter(associated_role=role):
        role_access[item.associated_service.service_name] = \
            str(item.access_level).split(",")
    return role_access


def access_results(request, role_id):
    """Find all systems that role needs access to"""
    role = Role.objects.get(pk=role_id)
    total_access = get_access(role)
    roles_checked = [role]
    while role.membership:
        if role.membership in roles_checked:
            """Prevent infinite loops if role is eventually member of itself"""
            response = "Role loop detected at %s!"
            return HttpResponse(response % role)
        privileges = get_access(role.membership)
        for privilege in privileges:
            if privilege in total_access:
                for priv in privileges[privilege]:
                    total_access[privilege].append(priv)
            else:
                total_access[privilege] = privileges[privilege]
        role = role.membership
        roles_checked.append(role)
    template = loader.get_template('rba/access.html')
    colors = {}
    owners = {}
    teams = []
    contacts = {}
    for team in Team.objects.all():
        teams.append(team.team_name)
    teams.append("")
    for key in total_access:
        try:
            colors[key] = Service.objects.get(service_name=key).service_color()
        except:
            colors[key] = "000000"
        try:
            owners[key] = Service.objects.get(service_name=key).service_team()
        except:
            owners[key] = ""
    for team in Team.objects.all():
        try:
            contacts[team.team_name] = team.contact_info
        except:
            contacts[team.team_name] = ""
    context = {
        'access': total_access,
        'role': Role.objects.get(pk=role_id).role_name,
        'colors': colors,
        'owners': owners,
        'teams': teams,
        'contacts': contacts,
    }
    return HttpResponse(template.render(context, request))


@register.filter
def get_item(dictionary, key):
    """For looking up dictionary values in templates"""
    return dictionary.get(key)

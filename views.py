#Copyright 2016 Matthew Krohn
#
#This file is part of RBATool.
#
#Basic Inventory is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
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


def build_members(role):
    """Figure out what members a primary role inherits"""
    members = [role]
    more_roles = Role.objects.filter(membership=role)
    roles_to_check = []
    for role in more_roles:
        roles_to_check.append(role)
    while len(roles_to_check) > 0:
        for new_role in roles_to_check:
            if new_role in members:
                return Role_Loop
            members.append(new_role)
            for new_member in Role.objects.filter(membership=new_role):
                roles_to_check.append(new_member)
            roles_to_check.remove(new_role)
    return members


def get_service_access(service, access):
    """Find all roles that need access to a service"""
    accesses = Access.objects.filter(associated_service=service)
    service_access = access
    for access in accesses:
        primary_role = access.associated_role
        roles = [primary_role]
        for member in build_members(primary_role):
            roles.append(member)
        for role in roles:
            if role.role_name in service_access:
                if access.access_level not in service_access[role.role_name]:
                    service_access[role.role_name].append(access.access_level)
            else:
                service_access[role.role_name] = [access.access_level]
    return service_access


def service_audit(request, service_id):
    """Load a webpage with all privileged roles to a service"""
    template = loader.get_template('rba/audit.html')
    service = Service.objects.get(pk=service_id)
    access = {}
    access = get_service_access(service, access)
    context = {
        'service': service.service_name,
        'access': access,
    }
    return HttpResponse(template.render(context, request))


def service_list(request):
    """List all services and links to audit pages"""
    service_list = Service.objects.order_by("service_name")
    template = loader.get_template('rba/services.html')
    context = {
        'service_list': service_list,
    }
    return HttpResponse(template.render(context, request))


@register.filter
def get_item(dictionary, key):
    """For looking up dictionary values in templates"""
    return dictionary.get(key)

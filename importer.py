from models import Service,Role,Access

def read_new_services(file):
    with open(file) as access_file:
        return access_file.readline().strip().split(",")[2:]

def read_current_services():
    current_services = []
    for service in Service.objects.all():
        current_services.append(service.service_name)
    return current_services

def import_services(service_list):
    current_services = read_current_services()
    for service in service_list:
        if service not in current_services:
            new_service = Service(service_name=service)
            new_service.save()

def read_new_roles(file):
    new_roles = {}
    with open(file) as access_file:
        for line in access_file.readlines()[1:]:
            try:
                new_roles[line.strip().split(",")[0]] = line.strip().split(",")[1]
            except:
                new_roles[line.strip().split(",")[0]] = ""
    return new_roles

def read_current_roles():
    current_roles = []
    for role in Role.objects.all():
        current_roles.append(role.role_name)
    return current_roles

def import_roles(role_list):
    current_roles = read_current_roles()
    for role in role_list:
        if role not in current_roles:
            new_role = Role(role_name=role)
            new_role.save()

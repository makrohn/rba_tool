from models import Service,Role,Access
"""Command-line only script to import database from csv"""

def read_new_services(file):
    """Open a file and load new services from first row"""
    with open(file) as access_file:
        return access_file.readline().strip().split(",")[2:]

def read_current_services():
    """Find out what current services are in django database"""
    current_services = []
    for service in Service.objects.all():
        current_services.append(service.service_name)
    return current_services

def import_services(service_list):
    """Add any services from file to django database"""
    current_services = read_current_services()
    for service in service_list:
        if service not in current_services:
            new_service = Service(service_name=service)
            new_service.save()

def read_new_roles(file):
    """Find new roles from 1st col of CSV and memberships from 2nd col"""
    new_roles = {}
    with open(file) as access_file:
        for line in access_file.readlines()[1:]:
            if line.strip().split(",")[1] == "":
                new_roles[line.strip().split(",")[0]] = None
            else:
                new_roles[line.strip().split(",")[0]] = line.strip().split(",")[1]
    return new_roles

def read_current_roles():
    """Read roles from django database"""
    current_roles = []
    for role in Role.objects.all():
        current_roles.append(role.role_name)
    return current_roles

def update_role(role, membership_check):
    """Make sure role membership in db is set to val from csv col 2"""
    role_check = Role.objects.get(role_name=role)
    if role_check.membership != membership_check:
        try:
            new_membership = Role.objects.get(role_name=membership_check)
            role_check.membership = new_membership
            role_check.save()
        except:
            new_role = Role(role_name=membership_check)
            new_role.save()
            new_membership = new_role
            role_check.membership = new_membership
            role_check.save()

def import_roles(role_dict):
    """Add any missing roles to django db"""
    for role in role_dict:
        try:
            update_role(role,role_dict[role])
        except:
            new_role = Role(role_name=role)
            new_role.save()
            update_role(role,role_dict[role])

def read_access_line(line, service_list):
    """Read a line from csv and figure out what services it needs privs to"""
    new_access = {}
    line_items = line.strip().split(",")[2:]
    for service in service_list:
        try:
            if line_items[service_list.index(service)] != "":
                service_name = service
                new_access[service_name] = line_items[service_list.index(service)]
        except:
            print "Error",line.strip().split(",")[0],service
    return line.strip().split(",")[0],new_access

def write_new_access(role_text,access_dict):
    """Use data from csv about a role to generate access objects for that role"""
    for service_text in access_dict:
        new_access = Access(
            associated_role = Role.objects.get(role_name=role_text),
            associated_service = Service.objects.get(service_name=service_text),
            access_level = access_dict[service_text]
            )
        new_access.save()

def write_all_access(file,service_list):
    """For all lines in a csv, write access objects"""
    with open(file) as access_file:
        for line in access_file.readlines()[1:]:
            access_data = read_access_line(line,service_list)
            role_name = access_data[0]
            access_dict = access_data[1]
            write_new_access(role_name,access_dict)

def import_csv(file):
    """Load csv, add all roles & services to db, add al access objects"""
    new_services = read_new_services(file)
    import_services(new_services)
    new_roles = read_new_roles(file)
    import_roles(new_roles)
    write_all_access(file,new_services)

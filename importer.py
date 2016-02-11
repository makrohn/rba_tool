from models import Service,Role,Access

def read_new_services(file):
    with open(file) as access_file:
        return access_file.readline().strip().split(",")

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

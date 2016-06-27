rba_tool
========

For calculating role-based access


Installation instructions:
==========================
Clone repo to "rba" folder

Add
'rba.apps.RbaConfig',
to INSTALLED_APPS in your project's setting.py

Add
    url(r'^rba/', include('rba.urls')),
to urlpatterns in your project's urls.py

python manage.py makemigrations rba
python manage.py migrate rba

Setup:
======
There are three objects you can create in Django admin:
Services: The servers or services that people have logins to (eg Google, LDAP, etc)
Roles: Categories that users might fall into who share the same access levels
Teams: A responsible team for a service and how to contact them.

Each role, in addition to being an object itself, can also be a member of another role.

End Usage:
==========
Once you've set up some Roles with access to some Servers, go to:
http://myserver/rba
And you should see a list of roles. Click any role to see a quick calculation of what access a person in that role should be granted, as well as, organizationally, what they might inherit.

http://myserver/rba/services
Will give you a list of services, so that someone can check which roles should have access to that service.

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

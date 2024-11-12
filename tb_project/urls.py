
# client_project/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts.views import login_user


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',login_user),
    path('admin/', admin.site.urls),
    path('client/', include('tb_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),


]


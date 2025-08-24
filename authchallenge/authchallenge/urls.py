from django.contrib import admin
from django.urls import path, include
from core.views import debug_hosts  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
        path("debug-hosts/", debug_hosts),
]

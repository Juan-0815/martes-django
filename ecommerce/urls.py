from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
 path('admin/', admin.site.urls),
    path('registration', include('registration.urls')),  # URLs de la aplicación de registro
    path('', include('store.urls')),  # Asegúrate de que esta sea la ruta correcta
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

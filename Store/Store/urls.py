from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='storeProducts/', permanent=False)),
    path('admin/', admin.site.urls),
    path('storeProducts/', include('storeProducts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

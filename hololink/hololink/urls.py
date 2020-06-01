from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('article/', include('article.urls')),
    path('', RedirectView.as_view(url='/article/')),
]
from django.urls import path, include
from django.contrib import admin
from .views import index, d3demo

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('article/', include('article.urls')),
    path('', index, name='index'),
    path('d3demo/', d3demo, name='d3demo'),
]

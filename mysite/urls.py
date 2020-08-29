"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^arm/', include('arm.urls')),
                  url(r'^$', include('personal.urls')),
                  url(r'^speka/', include('speka.urls')),
                  url(r'^armcalc/', include('armcalc.urls')),
                  url(r'^spectrum/', include('spectrum.urls')),
                  url(r'^materials/', include('materials.urls')),
                  url(r'^kvartira/', include('kvartira.urls')),
                  url(r'^colors/', include('colors.urls')),
                  url(r'^wind/', include('wind.urls')),
                  url(r'^spectrum_v17/', include('spectrum_v17.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

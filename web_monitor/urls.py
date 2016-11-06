from django.conf.urls import url
from django.contrib import admin
from report.views import get_web_data
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_web_data, name='home'),
]

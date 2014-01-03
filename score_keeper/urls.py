from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^players/', TemplateView.as_view(template_name="home.html"), name='players'),
    url(r'^games/', TemplateView.as_view(template_name="home.html"), name='games'),
    url(r'^admin/', include(admin.site.urls)),
)

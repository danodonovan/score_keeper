from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from keeper.views import PlayerListView, GoalListView, GameListView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^players/', PlayerListView.as_view(), name='players'),
    url(r'^games/', GameListView.as_view(), name='games'),
    url(r'^goals/', GoalListView.as_view(), name='goals'),
    url(r'^admin/', include(admin.site.urls)),
)
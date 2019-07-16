
from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^contact', views.ContactView.as_view(), name='contact'),
    url(r'^test', views.ContactView.as_view(), name='test'),
    url(r'^search/$',views.search,name='search'),
    url(r'^$', views.IndexView.as_view(), name='index'), #the second parameter must be the function, so use as_view
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^love', views.ContactView.as_view(), name='test2'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchievesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'), #view.category before
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag')]
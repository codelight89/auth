from django.conf.urls import patterns, include, url
from django.contrib import admin

from auth_app import views

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^home/$', views.IndexPageView.as_view(), name='index'),
                       url(r'^$', views.LoginFormView.as_view()),
                       url(r'^logout/$', views.LogoutView.as_view()),
                       url(r'^register/$', views.RegisterUserView.as_view(), name='register'),
                       url('^', include('django.contrib.auth.urls')),
                       url(r'^register_success/$', views.RegisterSuccess.as_view()),
                       url(r'^confirm/(?P<activation_key>\w+)/', views.RegisterConfirm.as_view()),
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       )

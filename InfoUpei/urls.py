__author__ = 'kent'

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import patterns,url
from InfoUpei import views

urlpatterns=patterns('',
                     url(r'^$',views.index,name='index'),
                     url(r'^user_login/$',views.user_login,name='user_login'),
                     url(r'^add_course/$',views.add_course,name='add_course'),
                     url(r'^course_menu/$',views.course_menu,name='course_menu'),
                     url(r'^register/$',views.register,name='register'),
                     url(r'^user_logout/$',views.user_logout,name='user_logout'),
                     url(r'^register_course/$',views.register_course,name='register_course'),
                     url(r'^error_page/$',views.error_page,name='error_page'),
                     url(r'^user/(?P<username>[\w\-]+)/$', views.user_detail, name='user_detail'),
                     url(r'^course/(?P<coursename>[\w\-]+)/$', views.course_detail, name='course_detail'),

)

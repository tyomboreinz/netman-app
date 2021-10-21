from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from ipam.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', list_user, name='users'),
    path('user/add', signup, name='signup'),
    path('user/delete/<str:username>', del_user, name='del_user'),
    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard', dashboard, name='dashboard'),
    path('', home, name='home'),

    path('network/', network_list, name='network_list'),
    path('network/add', network_add, name='network_add'),
    path('network/edit/<int:id_subnet>', network_edit, name='network_edit'),
    path('network/scan/<int:id_subnet>', network_scan , name='network_scan'),
    path('network/<int:id_subnet>', network_detail, name='detail_network'),
    path('network/delete/<int:id_subnet>', network_delete , name='network_delete'),

    path('ipaddress/add/', ip_add, name='ip_add'),
    path('ipaddress/delete/<int:id_ip>', ip_delete, name='ip_delete'),
    path('ipaddress/edit/<int:id_ip>', ip_edit, name='ip_edit'),

    path('applications', applications, name='applications'),
    path('application/add', application_add, name='app_add'),
    path('application/edit/<int:id_app>', application_edit, name='app_edit'),
    path('application/delete/<int:id_app>', application_delete, name='app_delete'),

    path('databases', databases, name='databases'),
    path('database/add', database_add, name='db_add'),
    path('database/edit/<int:id_db>', database_edit, name='db_edit'),
    path('database/delete/<int:id_db>', database_delete, name='db_delete'),

    path('config/portal/edit/<int:id_config>', config_edit, name='config_edit'),

    path('setting/', setting_os, name='setting'),
    path('os/delete/<int:id_os>', os_delete, name='os_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
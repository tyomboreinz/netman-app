from tokenize import group
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

    path('group/', group_list, name='group'),
    path('group/add', group_add, name='group_add'),
    path('group/active/<int:id_group>', group_active, name='group_active'),
    path('group/edit/<int:id_group>', group_edit, name='group_edit'),
    path('group/delete/<int:id_group>', group_delete, name='group_delete'),

    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('starting_up', starting_up, name='starting_up'),
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

    path('credentials', credentials, name='credentials'),
    path('credential/add', credential_add, name='cred_add'),
    path('credential/edit/<int:id_cred>', credential_edit, name='cred_edit'),
    path('credential/delete/<int:id_cred>', credential_delete, name='cred_delete'),

    path('config/portal/edit/<int:id_config>', config_edit, name='config_edit'),

    path('setting/', setting_os, name='setting'),
    path('os/delete/<int:id_os>', os_delete, name='os_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
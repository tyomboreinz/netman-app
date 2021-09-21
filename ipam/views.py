from django.db.models.aggregates import Count
from django.contrib.auth.models import User
from ipam.network import Network
from django.shortcuts import render, redirect
from django.db.models.functions import Length
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from ipam.models import *
from ipam.forms import *
from django.contrib.auth import get_user_model
import datetime, random, ipcalc

@staff_member_required(login_url=settings.LOGIN_URL)
def del_user(request, username):
    userdelete = User.objects.get(username=username)
    userdelete.delete()
    return redirect('/users/')

@login_required(login_url=settings.LOGIN_URL)
def list_user(request):
    listuser = get_user_model().objects.exclude(username=request.user)
    data = {
        'menu_user' : 'class=mm-active',
        'current_user' : request.user,
        'list_user' : listuser,
    }
    
    return render(request, 'list_user.html', data)

@login_required(login_url=settings.LOGIN_URL)
def signup(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/')
        else:
            messages.error(request, "Check again your password !")
            return redirect('/user/add')
    else:
        form = UserCreationForm()
        data = {
            'form' : form,
            'title' : 'Add User',
            'subtitle' : 'Add User to access this Application',
        }
    
    return render(request,'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def os_delete(request, id_os):
    os = OS.objects.get(id=id_os)
    os.delete()
    return redirect('/setting')

@login_required(login_url=settings.LOGIN_URL)
def setting_os(request):
    if request.POST:
        form = FormOS(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/setting')
    else:
        form = FormOS()
        data = {
            'menu_config' : 'class=mm-active',
            'form' : form,
            'os_data' : OS.objects.all().order_by('name'),
            'configs' : ConfigPortal.objects.all().order_by('config'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            }
    return render(request, 'setting.html', data)

@login_required(login_url=settings.LOGIN_URL)
def config_edit(request, id_config):
    set = ConfigPortal.objects.get(id=id_config)
    if request.POST:
        form = FormConfigs(request.POST, instance=set)
        if form.is_valid():
            form.save()
            return redirect('/setting')
    else:
        form = FormConfigs(instance=set)
        data = {
            'form' : form,
            'title' : 'Edit Config Portal - ' + str(set.config).upper(),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def application_delete(request, id_app):
    app = Application.objects.get(id=id_app)
    if app.image:
        app.image.delete()
    app.delete()
    return redirect('applications')

@login_required(login_url=settings.LOGIN_URL)
def application_edit(request, id_app):
    app = Application.objects.get(id=id_app)
    if request.POST:
        post_value = request.FILES.copy()
        if post_value:
            app.image.delete()
        form = FormApplication(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('applications')
    else:
        form = FormApplication(instance=app)
        data = {
            'form' : form,
            'title' : 'Edit App',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def application_add(request):
    if request.POST:
        form = FormApplication(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('applications')
    else:
        form = FormApplication()
        data = {
            'form' : form,
            'title' : 'Add App',
            'subtitle' : 'Adding Applications',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def applications(request):
    data = {
        'app_list' : Application.objects.all(),
        'menu_app' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'applications.html', data)

@login_required(login_url=settings.LOGIN_URL)
def ip_delete(request, id_ip):
    ip = Ip_address.objects.get(id=id_ip)
    ip.delete()
    return redirect('/network/' + str(ip.subnet_id))

@login_required(login_url=settings.LOGIN_URL)
def ip_edit(request, id_ip):
    ip = Ip_address.objects.get(id=id_ip)
    if request.POST:
        form = FormIpAddress(request.POST, instance=ip)
        if form.is_valid():
            subnet = Subnet.objects.get(ip_network=form.cleaned_data['subnet'])
            form.save()
            return redirect('/network/' + str(subnet.id))
    else:
        form = FormIpAddress(instance=ip)
        data = {
            'form' : form,
            'ip' : ip,
            'title' : 'Edit IP Address',
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def ip_add(request):
    if request.POST:
        form = FormIpAddress(request.POST)
        if form.is_valid():
            subnet = Subnet.objects.get(ip_network=form.cleaned_data['subnet'])
            form.save()
            return redirect('/network/' + str(subnet.id))
    else:
        form = FormIpAddress()
        data = {
            'form' : form,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Add IP',
            'subtile' : 'Adding IP Address to manage'
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_delete(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    subnet.delete()
    return redirect('/network/')

@login_required(login_url=settings.LOGIN_URL)
def network_edit(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    if request.POST:
        post_value = request.POST.copy()
        subnet_calc = ipcalc.Network(str(post_value['ip_network']+'/'+str(post_value['netmask'])))
        post_value['ip_network'] = str(subnet_calc.network())
        post_value['ip_broadcast'] = str(subnet_calc.broadcast())
        form = FormSubnet(post_value, instance=subnet)
        if form.is_valid():
            form.save()
            return redirect('/network')
    else:
        form = FormSubnet(instance=subnet)
        data = {
            'form' : form,
            'subnet' : subnet,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Edit Network',
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_detail(request, id_subnet):
    ips = Ip_address.objects.filter(subnet=id_subnet).order_by(Length('ip_address').asc(), 'ip_address')
    data = {
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'id_subnet' : id_subnet,
        'ips' : ips,
        'menu_network_detail' : 'class=mm-active',
        'menu_network_' : 'class=mm-active',
    }
    return render(request, 'network-detail.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_add(request):
    if request.POST:
        post_value = request.POST.copy()
        subnet = ipcalc.Network(str(post_value['ip_network']+'/'+str(post_value['netmask'])))
        post_value['ip_network'] = str(subnet.network())
        post_value['ip_broadcast'] = str(subnet.broadcast())
        form = FormSubnet(post_value)
        if form.is_valid():
            form.save()
            return redirect('/network/')
    else:
        form = FormSubnet()
        form.fields['ip_broadcast'].widget = forms.HiddenInput()
        data = {
            'form' : form,
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Add Network',
            'subtitle' : 'Adding Network to more connect with other'
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_list(request):
    subnets = Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network')
    data = {
        'subnets' : subnets,
        'sidebar_subnets' : subnets,
        'menu_network_list' : 'class=mm-active',
        'menu_network' : 'class=mm-active',
    }
    return render(request, 'network-list.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_scan(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    existing_ip = Ip_address.objects.filter(subnet=id_subnet)
    lists_ip = Network.network_scan(subnet.ip_network +"/"+ subnet.netmask)

    for ip in lists_ip:
        token = 0
        for address in existing_ip:
            if ip == address.ip_address:
                token += 1

        if token == 0:
            Ip_address.objects.create(ip_address=str(ip),subnet_id=id_subnet)
            print("IP : "+ ip +" Addedd Successfully")
        else:
            print("IP : "+ ip +" Already Available")
        
    return redirect('/network/'+ str(id_subnet))

@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    os = OS.objects.all().annotate(count_os=Count('ip_address')).order_by('-count_os')
    total_ip = Ip_address.objects.all().count()
    color_list = ['#007bff', '#6610f2', '#6f42c1', '#e83e8c', '#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997', '#17a2b8', '#6c757d', '#3f6ad8', '#6c757d', '#3ac47d', '#16aaff', '#f7b924', '#d92550', '#eee', '#343a40', '#444054', '#794c8a']
    data_os = []
    for data in os:
        count_data = Ip_address.objects.filter(os_id=data.id).count()
        if count_data != 0:
            data_os.append({'name' : data.name, 'count' : count_data})
    
    color = random.sample(color_list, len(data_os))
    for i in range(len(data_os)):
        data_os[i]['color'] = color[i]

    data = {
        'total_subnet' : Subnet.objects.all().count(),
        'total_ip' : total_ip,
        'total_app' : Application.objects.all().count(),
        'data_os' : data_os,
        'menu_dashboard' : 'class=mm-active',
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dashboard.html', data)

def home(request):
    now = datetime.datetime.now()
    data = {
        'company_name' : ConfigPortal.objects.get(config='company_name'),
        'company_short_name' : ConfigPortal.objects.get(config='company_short_name'),
        'company_address' : ConfigPortal.objects.get(config='company_address'),
        'company_telp' : ConfigPortal.objects.get(config='company_telp'),
        'company_email' : ConfigPortal.objects.get(config='company_email'),
        'company_website' : ConfigPortal.objects.get(config='company_website'),
        'app_name' : ConfigPortal.objects.get(config='portal_name'),
        'app_list' : Application.objects.all(),
        'year' : now.year
    }
    return render(request, 'portal.html', data)
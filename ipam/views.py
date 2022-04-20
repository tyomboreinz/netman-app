from ipaddress import ip_address
from django.db.models.aggregates import Count
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models.functions import Length
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from ipam.models import *
from ipam.forms import *
from ipam.crypt import Crypt
from django.contrib.auth import get_user_model
import datetime, random, ipcalc, subprocess

@login_required(login_url=settings.LOGIN_URL)
def group_list(request):
    data = {
        'group_list' : Group.objects.all(),
        'menu_group' : 'class=mm-active',
        'active_group' : Group.objects.get(is_active=1),
        'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'group.html', data)

@login_required(login_url=settings.LOGIN_URL)
def group_active(request, id_group):
    Group.objects.filter(is_active=1).update(is_active=0)
    Group.objects.filter(id=id_group).update(is_active=1)
    return redirect('/group/')

@login_required(login_url=settings.LOGIN_URL)
def group_add(request):
    if request.POST:
        form = FormGroup(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('group')
    else:
        form = FormGroup()
        data = {
            'form' : form,
            'title' : 'Add Group',
            'subtitle' : 'Adding Group',
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def group_edit(request, id_group):
    set = Group.objects.get(id=id_group)
    if request.POST:
        form = FormGroup(request.POST, instance=set)
        if form.is_valid():
            form.save()
            return redirect('/group')
    else:
        form = FormGroup(instance=set)
        data = {
            'form' : form,
            'title' : 'Edit Group',
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@staff_member_required(login_url=settings.LOGIN_URL)
def group_delete(request, id_group):
    group = Group.objects.get(id=id_group)
    group.delete()
    return redirect('/group/')

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
        'active_group' : Group.objects.get(is_active=1),
        'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
        if request.FILES:
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
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def application_add(request):
    group_ = Group.objects.get(is_active=1)
    if request.POST:
        form = FormApplication(request.POST, request.FILES)
        if form.is_valid():
            new_app = form.save()
            Application.objects.filter(id=new_app.id).update(group=group_.id)
            return redirect('applications')
    else:
        form = FormApplication()
        ips = Ip_address.objects.filter(subnet__group__is_active=1).values('id', 'ip_address').order_by(Length('ip_address').asc(), 'ip_address')
        list_choices = ()
        for ip in ips:
            address = (str(ip['id']), ip['ip_address'])
            list_choices += (address,)
        form.fields['ip'].choices = list_choices
        data = {
            'form' : form,
            'title' : 'Add App',
            'subtitle' : 'Adding Applications',
            'active_group' : group_,
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def applications(request):
    data = {
        'active_group' : Group.objects.get(is_active=1),
        # 'app_list' : Application.objects.filter(ip__subnet__group__is_active=1),
        'app_list' : Application.objects.filter(group__is_active=1),
        'menu_app' : 'class=mm-active',
        'active_group' : Group.objects.get(is_active=1),
        'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'applications.html', data)

@login_required(login_url=settings.LOGIN_URL)
def credential_delete(request, id_cred):
    cred = Credential.objects.get(id=id_cred)
    cred.delete()
    return redirect('credentials')

@login_required(login_url=settings.LOGIN_URL)
def credential_edit(request, id_cred):
    cred = Credential.objects.get(id=id_cred)
    if request.POST:
        post_value = request.POST.copy()
        post_value['owner'] = request.user
        form = FormCredential(post_value, instance=cred)
        if form.is_valid():
            form.save()
            return redirect('credentials')
    else:
        form = FormCredential(instance=cred)
        data = {
            'form' : form,
            'title' : 'Edit Credential',
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def credential_add(request):
    if request.POST:
        post_value = request.POST.copy()
        string_pass = post_value['password']
        post_value['password'] = Crypt.encrypt_string(string_pass)
        post_value['owner'] = request.user
        form = FormCredential(post_value)
        if form.is_valid():
            form.save()
            return redirect('credentials')
    else:
        form = FormCredential()
        ips = Ip_address.objects.filter(subnet__group__is_active=1).values('id', 'ip_address').order_by(Length('ip_address').asc(), 'ip_address')
        list_choices = ()
        for ip in ips:
            address = (str(ip['id']), ip['ip_address'])
            list_choices += (address,)
        form.fields['ip'].choices = list_choices
        form.fields['owner'].widget = forms.HiddenInput()
        data = {
            'form' : form,
            'title' : 'Add Credential',
            'subtitle' : 'Adding Credential',
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def credentials(request):
    list_cred = Credential.objects.filter(owner=request.user, id=46, ip__subnet__group__is_active=1).values('id','type','ip__ip_address','username','password','description','ip__hostname').order_by('ip__ip_address', 'type')
    for cred in list_cred:
        string_pass = cred['password']
        cred['password'] = Crypt.decrypt_string(string_pass)
    data = {
        # 'cred_list' : Credential.objects.filter(owner=request.user, ip__subnet__group__is_active=1).values('id','type','ip__ip_address','username','password','description','ip__hostname').order_by('ip__ip_address', 'type'),
        'cred_list' : list_cred,
        'menu_cred' : 'class=mm-active',
        'active_group' : Group.objects.get(is_active=1),
        'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'credentials.html', data)

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
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
        ips = Subnet.objects.filter(group__is_active=1).values('id', 'ip_network', 'description').order_by(Length('ip_network').asc(), 'ip_network')
        list_choices = ()
        for ip in ips:
            address = (str(ip['id']), ip['ip_network'] +" - "+ ip['description'])
            list_choices += (address,)
        form.fields['subnet'].choices = list_choices
        data = {
            'form' : form,
            'active_group' : Group.objects.get(is_active=1),
            'active_subnet' : ConfigPortal.objects.get(config="active_subnet"),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
        form.fields['group'].widget = forms.HiddenInput()
        data = {
            'form' : form,
            'subnet' : subnet,
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Edit Network',
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_detail(request, id_subnet):
    ConfigPortal.objects.filter(config="active_subnet").update(value=id_subnet)
    ips = Ip_address.objects.filter(subnet=id_subnet,subnet__group__is_active=1).order_by(Length('ip_address').asc(), 'ip_address')
    data = {
        'active_group' : Group.objects.get(is_active=1),
        'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
        post_value['group'] = str(getattr(Group.objects.get(is_active=1), 'id'))
        form = FormSubnet(post_value)
        if form.is_valid():
            form.save()
            return redirect('/network/')
    else:
        form = FormSubnet()
        form.fields['ip_broadcast'].widget = forms.HiddenInput()
        form.fields['group'].widget = forms.HiddenInput()
        data = {
            'form' : form,
            'active_group' : Group.objects.get(is_active=1),
            'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Add Network',
            'subtitle' : 'Adding Network to more connect with other'
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_list(request):
    subnets = Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network')
    data = {
        'active_group' : Group.objects.get(is_active=1),
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

    x = subprocess.check_output("nmap -sn "+ subnet.ip_network +"/"+ subnet.netmask +""" | grep report | awk '{print $NF}' | sed 's/(//g' | sed 's/)//g' """, shell=True, text=False)
    x_decode = x.decode("utf-8")
    lists_ip = list(filter(None,(x_decode.split("\n"))))

    for ip in lists_ip:
        token = 0
        for address in existing_ip:
            if ip == address.ip_address:
                token += 1

        if token == 0:
            Ip_address.objects.create(ip_address=str(ip),subnet_id=id_subnet)
            print("IP : "+ ip +" Addedd Successfully")
        else:
            print("IP : "+ ip +" Already Exist")
        
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
        'active_group' : Group.objects.get(is_active=1),
        'sidebar_subnets' : Subnet.objects.filter(group__is_active=1).order_by(Length('ip_network').asc(), 'ip_network'),
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
        'app_list' : Application.objects.order_by('group__name','name'),
        'year' : now.year
    }
    return render(request, 'portal.html', data)

def starting_up(request):
    start = ConfigPortal.objects.get(config='started_up')
    if str(start) == '0':
        Crypt.generate_key()
        ConfigPortal.objects.filter(config='started_up').update(value=1)

    return redirect('/dashboard')
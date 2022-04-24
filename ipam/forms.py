from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from ipam.models import *

class FormIpAddress(ModelForm):

    description = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Ip_address
        fields = '__all__'

        widgets = {
            'ip_address': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'hostname': forms.TextInput({'class':'form-control'}),
            'subnet': forms.Select({'class':'form-control'}),
            'os': forms.Select({'class':'form-control'}),
        }

class FormSubnet(ModelForm):

    description = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Subnet
        fields = '__all__'

        netmask = ()
        for i in range(0, 32):
            net = (str(i), str(i))
            netmask += (net,)

        labels = {
            'ip_network' : "IP "
        }
        
        widgets = {
            'netmask': forms.Select(choices=netmask,attrs={'class':'form-control'}),
            'ip_network': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'ip_broadcast': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
        }

class FormApplication(ModelForm):

    domain = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    description = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Application
        fields = '__all__'

        exclude = ['group']
        
        list_choices = (
            ('http', 'http'),
            ('https', 'https'), )

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'protocol': forms.Select(choices=list_choices,attrs={'class':'form-control'}),
            'port': forms.TextInput({'class':'form-control'}),
            'ip': forms.Select({'class':'multiselect-dropdown form-control'}),
        }

class FormConfigs(ModelForm):
    class Meta:
        model = ConfigPortal
        fields = ['value']
        widgets = {
            'value' : forms.TextInput({'class':'form-control'})
        }

class FormOS(ModelForm):
    class Meta:
        model = OS
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control', 'placeholder':'Press Enter to add OS'}),
        }

class FormCredential(ModelForm):

    description = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Credential
        fields = '__all__'

        widgets = {
            'type': forms.TextInput({'class':'form-control'}),
            'ip': forms.Select({'class':'multiselect-dropdown form-control'}),
            'username': forms.TextInput({'class':'form-control'}),
            'password': forms.PasswordInput({'class':'form-control','data-toggle':'password'}),
        }

class FormGroup(ModelForm):

    description = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Group
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username Here ...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Here ...'}))

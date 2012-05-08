from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
import re
from django.core.validators import email_re

email_separator_re = re.compile(r'[^\w\.\-\+@_]+')

def _is_valid_email(email):
    return email_re.match(email)

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email",required=True)
    password = forms.CharField(label="Parola",widget=forms.PasswordInput,required=True)

    def __init__(self,*args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)

    def clean(self):
        self.email = self.cleaned_data.get('email')
        self.password = self.cleaned_data.get('password')

        if self.email and self.password:
            try:
                user = User.objects.get(email=self.email)
            except:
                self._errors["email"] =  self.error_class([_("login_err_username_not_found")])
                return self.cleaned_data

            user = authenticate(email=self.email, password=self.password)
            if user is None:
                self._errors["password"] =  self.error_class([_("login_err_password")])
        return self.cleaned_data


class RegisterForm(forms.Form):
    email = forms.EmailField(help_text=_('PleaseEnterEmail'))
    first_name = forms.CharField(label='Isim', max_length=100)
    last_name = forms.CharField(label='Soyisim', max_length=100)
    password = forms.CharField(label='Parola', max_length=32, widget=forms.PasswordInput,)
    password_again = forms.CharField(label='Parola (tekrar)', max_length=32, widget=forms.PasswordInput, help_text=_('AtLeastFive1'))

    def clean_email(self):
        field_data = self.cleaned_data['email']

        if not field_data:
            return ''

        u = User.objects.filter(email=field_data)
        if len(u) > 0:
            raise forms.ValidationError(_('AlreadyRegisteredEmail'))

        return field_data

    def clean_password_again(self):
        field_data = self.cleaned_data['password_again']

        if not self.cleaned_data.has_key('password'):
            return
        else:
            password = self.cleaned_data['password']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Parolada bosluk olmamalidir")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Parola en az 5 karakter olmalidir")

        if (password or field_data) and password != field_data:
                    raise forms.ValidationError(u"Parolalar eslesmiyor")

        return field_data   
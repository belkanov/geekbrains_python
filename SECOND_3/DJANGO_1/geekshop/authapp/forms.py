from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, ValidationError, UserChangeForm
from django import forms
import random, hashlib
from .models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ['username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar']

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, commit=True):
        user = super(ShopUserRegisterForm, self).save(commit=False)
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(str(user.email + salt).encode('utf8')).hexdigest()
        if commit:
            user.save()
        return user


class ShopUserChangeForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class ShopUserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ['tagline', 'about_me', 'sex']

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, ValidationError, UserChangeForm
from django import forms

from .models import ShopUser


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

    # я сделал валидатор в модели
    #
    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 18:
    #         raise ValidationError('Надо подрасти =) 18+')
    #
    #     return data


class ShopUserChangeForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ['username', 'first_name', 'email', 'age', 'avatar', 'password']

    def __init__(self, *args, **kwargs):
        super(ShopUserChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

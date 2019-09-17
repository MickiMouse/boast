from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import BoastUser, user_registrated


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput,
                                help_text='Write your password')

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            errors = {'password2': ValidationError('Passwords do not match',
                                                   code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = BoastUser
        fields = ('username', 'email', 'password', 'password2',
                  'first_name', 'last_name')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BoastUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'avatar')

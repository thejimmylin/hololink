from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpWithEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(f'This Email has already been used.')
        return email

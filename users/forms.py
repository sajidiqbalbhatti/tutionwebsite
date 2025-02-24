from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

    # Custom clean method to ensure password and confirmation password match
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password

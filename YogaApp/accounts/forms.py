from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Profile


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    profile_picture = forms.URLField(required=False, label="Profile Picture")

    class Meta:
        model = UserProfile
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                profile_picture=self.cleaned_data.get('profile_picture'),
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.URLInput(attrs={'class': 'form-control'}),
        }







from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.models import *

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field','placeholder': 'Enter Username','required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field','placeholder': 'Enter Password','required': True}))

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class PatientProfileFillUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Patient
        fields = [
            'date_of_birth', 'country', 'region', 'province', 
            'city_municipality', 'barangay', 'postal_code',
            'house_number_street', 'subdivision', 'contact_number', 
            'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

        self.fields['date_of_birth'] = forms.DateField(
            widget=forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            required=True
)
        self.fields['country'] = forms.ModelChoiceField(
            queryset=CountryOfBirth.objects.all(),
            widget=forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select Country'}),
            required=True
        )
        self.fields['region'] = forms.ModelChoiceField(
            queryset=Region.objects.all(),
            widget=forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select Region'}),
            required=True
        )
        self.fields['province'] = forms.ModelChoiceField(
            queryset=Province.objects.all(),
            widget=forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select Province'}),
            required=True
        )
        self.fields['city_municipality'] = forms.ModelChoiceField(
            queryset=CityMunicipality.objects.all(),
            widget=forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select City/Municipality'}),
            required=True
        )
        self.fields['barangay'] = forms.ModelChoiceField(
            queryset=Barangay.objects.all(),
            widget=forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select Barangay'}),
            required=True
        )
        self.fields['postal_code'] = forms.ModelChoiceField(
            queryset=PostalCode.objects.all(),
            widget=forms.Select(attrs={'class': 'input-field', 'placeholder': 'Select Postal Code'}),
            required=True
        )

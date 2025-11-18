from django import forms
from django.contrib.auth.models import User as AuthUser
import requests # Import requests to handle potential API errors
from .models import Profile, Car, CarPhoto, CustomerLead
from .services import fetch_vehicle_by_vin

class CarForm(forms.ModelForm):
    make = forms.CharField(required=False)
    model = forms.CharField(required=False)
    trim = forms.CharField(required=False)

    class Meta:
        model = Car
        fields = ['vin', 'year', 'make', 'model', 'trim', 'mileage', 'price', 'cash_down', 'condition', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vin'].required = True
        self.fields['year'].required = True
        self.fields['mileage'].required = True
        for name in ['make', 'model', 'trim', 'price', 'condition', 'status']:
            self.fields[name].required = False

    def clean(self):
        cleaned = super().clean()
        vin = cleaned.get('vin')
        
        if vin:
            try:
                data = fetch_vehicle_by_vin(vin) or {}
            except requests.exceptions.RequestException as e:
                print(f"Warning: VIN lookup failed due to API error: {e}")
                data = {}
            cleaned['make']  = cleaned.get('make')  or data.get('make')
            cleaned['model'] = cleaned.get('model') or data.get('model')
            cleaned['year']  = cleaned.get('year')  or data.get('year')
        required_fields = ['vin', 'year', 'mileage']
        for field in required_fields:
            value = cleaned.get(field)
            if not value:
                self.add_error(field, f'{field.title()} is required.')
                
        return cleaned

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'dealership_name', 'bio', 'avatar']

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name', 'email']

class CustomerLeadForm(forms.ModelForm):
    class Meta:
        model = CustomerLead
        fields = ['first_name', 'last_name', 'email', 'interested_in', 'status']

class CarPhotoForm(forms.ModelForm):
    class Meta:
        model = CarPhoto
        fields = ['image', 'caption']

class CarPhotoEditForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = CarPhoto
        fields = ["image", "caption"]

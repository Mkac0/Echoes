from django import forms
from django.contrib.auth.models import User as AuthUser
from .models import Profile, Car, CarPhoto, CustomerLead
from .services import fetch_vehicle_by_vin

class CarForm(forms.ModelForm):
    auto_import_photo = forms.BooleanField(
        required=False, initial=True,
        label='Auto-import'
    )
    class Meta:
        model = Car
        fields = ['make', 'model', 'trim', 'year', 'vin', 'mileage', 'price', 'condition', 'status']
    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        if not vin or len(vin) != 17:
            return {"error": "VIN must be 17 characters."}

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

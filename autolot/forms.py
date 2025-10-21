from django import forms
from django.contrib.auth.models import User as AuthUser
from .models import Profile, Car, CarPhoto, User
from .services import fetch_vehicle_by_vin

class CarForm(forms.ModelForm):
    auto_import_photo = forms.BooleanField(
        required=False, initial=True,
        label='Auto-import first photo from VIN API'
    )
    class Meta:
        model = Car
        fields = ['make', 'model', 'trim', 'year', 'vin', 'mileage', 'price', 'condition', 'status']
    
    def clean(self):
        cleaned_data = super().clean()
        vin = cleaned_data.get('vin')

        if vin:
            data = fetch_vehicle_by_vin(vin)
            cleaned_data['make'] = data.get('make', cleaned_data.get('make'))
            cleaned_data['model'] = data.get('model', cleaned_data.get('model'))
            cleaned_data['year'] = data.get('year', cleaned_data.get('year'))
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'dealership_name', 'bio', 'avatar']

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name', 'email']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'interested_in', 'status']

class CarPhotoForm(forms.ModelForm):
    class Meta:
        model = CarPhoto
        fields = ['image']

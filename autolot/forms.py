from django import forms
from .models import Car, CarPhoto, User
from .services import fetch_vehicle_by_vin

class CarForm(forms.ModelForm):
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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'interested_in', 'status']

class CarPhotoForm(forms.ModelForm):
    class Meta:
        model = CarPhoto
        fields = ['image']

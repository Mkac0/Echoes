from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

def avatar_upload_to(instance, filename):
    return f'avatars/user_{instance.user_id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True)
    dealership_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)

    def __str__(self):
        return self.name or self.user.get_username()
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile-detail')

class Car(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        PENDING = 'pending', 'Pending'
        SOLD = 'sold', 'Sold'
    
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    trim = models.CharField(max_length=50, blank=True)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900)])
    vin = models.CharField('VIN', max_length=17, unique=True)
    mileage = models.PositiveBigIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    condition = models.CharField(max_length=20, default='Used')
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.AVAILABLE)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} {self.vin}"
    
class CarPhoto(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="cars/")
    caption = models.CharField(max_length=120, blank=True, null=True)

class User(models.Model):
    class UserStatus(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        QUALIFIED = 'qualified', 'Qualified'

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(blank=True)
    interested_in = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    status = models.CharField(max_length=12, choices=UserStatus.choices, default=UserStatus.NEW)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

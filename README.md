# Echoes
![Echoes](https://i.imgur.com/oMFMeTp.png)

Echos is a CRUD application built with Django that allows users to create, read, update, and delete car listings. Users can see car listing with its VIN, mileage, and price. Users are also able to create/log into their account and create their own listings.


Selling cars made easy.

[Deployed App](https://echoes-644fddc8796a.herokuapp.com/) | [Project Planning](https://trello.com/b/NmoDQrSz/echoes)


## Why Echoes
My dad fixes and sells cars for a living. He mostly shows clients pictures of cars on his phone and spends a lot of time explaining the details. This app makes selling cars, easy.
Building Echoes taught me how to combine backend logic, user authentication, and external data integration into a single, production-ready platform.


### Attributions

+ Model Relationships – Learned to link Django models with ForeignKey and OneToOneField to connect users, profiles, and cars.

  - Using Django’s OneToOneField and signals, you can automatically create and link a Profile for each new User. This ensures every user has a corresponding profile without needing manual setup, keeping your data consistent and relationships clean.
  
  ***Example***
  
      from django.contrib.auth.models import User
      from myapp.models import Profile, Car
      
      user = User.objects.create(username="alex")
      profile = Profile.objects.create(user=user, bio="Car enthusiast")
      
      Car.objects.create(owner=profile, make="Tesla", model="Model S", year=2022)
      Car.objects.create(owner=profile, make="BMW", model="M3", year=2021)
      
      profile.cars.all()
      
  For more information on OneToOneField vs ForeignKey vs ManyToMany, visit [Understanding Django Relationships](https://dev.to/highcenburg/understanding-django-relationships-onetoonefield-vs-foreignkey-vs-manytomanyfield-4ifh).

+ API Integration - Integrated auto.dev API to automatically retrieve car details (make, model, year, and trim) by VIN

  - Used the requests library to make authenticated GET requests and parse the returned JSON into Django models.
  
  ***Example***
  
        import requests

        headers = {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'https://api.auto.dev/vin/3GCUDHEL3NG668790',
            headers=headers
        )
        
        result = response.json()
        print(result)
  

  - Handled cases where VINs were invalid or data was missing using graceful error messages and validation logic.
    For more information on Auto.dev API, visit [Auto.dev API Documentation](https://docs.auto.dev/v2).

+ User Authentication & Profiles – Implemented registration, login/logout, and profile pages that dynamically show each user’s vehicles.

  - By combining Django’s built-in authentication system (registration, login/logout) with model relationships (linking vehicles to users via ForeignKey), you can create personalized profile pages that dynamically display each user’s associated items (e.g., cars) in a secure and maintainable way.

  ***Example***
    
        class Car(models.Model):
          owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='cars')
          make = models.CharField(max_length=50)
          model = models.CharField(max_length=50)
          year = models.IntegerField()
      
          def __str__(self):
              return f"{self.make} {self.model} ({self.year})"
    
  For more information on User Authentication & Profiles, visit [How to USe a Foreign Key in Django](https://www.freecodecamp.org/news/how-to-use-a-foreign-key-in-django/) and [User Authentication System using Django](https://www.geeksforgeeks.org/python/user-authentication-system-using-django/).

+ Form Handling – Built custom ModelForms to validate user input and connect seamlessly with API responses.

  - Using a `ModelForm` ties your form fields and validation to your data model, and combining that with custom validation and an eternal API-data allows you to handle user input more safely.

  ***Example***
    
          def add_vehicle(request):
            if request.method == 'POST':
                form = VehicleForm(request.POST)
                if form.is_valid():
                    vehicle = form.save(commit=False)
                    vehicle.owner = request.user
                    vehicle.save()
                    return redirect('vehicle_list')
            else:
                api_response = requests.get("https://someapi.example.com/latest-car-models").json()
                initial_data = {
                    'make': api_response.get('make'),
                    'model': api_response.get('model'),
                    'year': api_response.get('year'),
                }
                form = VehicleForm(initial=initial_data)

    For more information on Form Handling, visit [django docs: ModelForm](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/).

+ Media & File Uploads – Added functionality for users to upload and manage car images and profile photos.

  - By using Django’s built-in ImageField/FileField on models, configuring MEDIA_ROOT/MEDIA_URL, and handling the uploaded files via request.FILES in forms and views, you can enable users to upload and manage images (for example profile photos and car pictures) in a secure and maintainable way.

  ***Example***
      
        @login_required
      def edit_profile(request):
          profile = request.user.profile
          if request.method == "POST":
              form = ProfileForm(request.POST, request.FILES, instance=profile)
              if form.is_valid():
                  form.save()
                  return redirect('profile')
          else:
              form = ProfileForm(instance=profile)
          return render(request, 'edit_profile.html', {'form': form})
  
  For more information on Media & File Uploads, visit [Geekforgeeks: Uploading images in Django - Python](https://www.geeksforgeeks.org/python/python-uploading-images-in-django/).

### Technologies
+ Python
+ Django
+ Heroku - App Deployment
+ Git/GitHub

### Next Steps
Planned features and stretch goals:
- Add an Admin/Lead user (to manage who is allowed to use the app & avoid scammers)
- Include "Send seller message" throught the App
- Include car detail notes/comments to elaborate on the condition of the car

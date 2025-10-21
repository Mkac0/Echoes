from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path("cars/", views.CarList.as_view(), name="car-list"),
    path("cars/new/", views.CarCreate.as_view(), name="car-create"),
    path("cars/<int:pk>/", views.CarDetail.as_view(), name="car-detail"),
    path("cars/<int:pk>/edit/", views.CarUpdate.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", views.CarDelete.as_view(), name="car-delete"),
    path("cars/<int:pk>/photos/new/", views.CarPhotoCreate.as_view(), name="carphoto-create"),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/new/", views.UserCreate.as_view(), name="user-create"),
    path("users/<int:pk>/edit/", views.UserUpdate.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDelete.as_view(), name="user-delete"),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profile/edit/', views.ProfileEdit.as_view(), name='profile-edit'),
]

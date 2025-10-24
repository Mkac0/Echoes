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
    path("leads/", views.CustomerLeadList.as_view(), name="customerlead-list"),
    path("leads/new/", views.CustomerLeadCreate.as_view(), name="customerlead-create"),
    path("leads/<int:pk>/edit/", views.CustomerLeadUpdate.as_view(), name="customerlead-update"),
    path("leads/<int:pk>/delete/", views.CustomerLeadDelete.as_view(), name="customerlead-delete"),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/', views.ProfilePublicDetail.as_view(), name='profile-public'),
    path('profile/edit/', views.ProfileEdit.as_view(), name='profile-edit'),
    path("cars/photos/<int:pk>/edit/", views.CarPhotoUpdate.as_view(), name="carphoto-update"),
    path("cars/photos/<int:pk>/delete/", views.CarPhotoDelete.as_view(), name="carphoto-delete"),
]

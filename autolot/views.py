from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Car, User, CarPhoto
from .forms import CarForm, UserForm, CarPhotoForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginView):
    template_name = 'home.html'

class CarList(ListView):
    model = Car
    template_name = "autolot/car_list.html"
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if q:
            qs = qs.filter(Q(make__icontains=q) | Q(model__icontains=q) | Q(vin__icontains=q))
        if status:
            qs = qs.filter(status=status)
        return qs

class CarDetail(DetailView):
    model = Car
    template_name = "autolot/car_detail.html"

class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = "autolot/form.html"
    success_url = reverse_lazy("car-list")

class CarUpdate(UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("car-list")

class CarDelete(DeleteView):
    model = Car
    success_url = reverse_lazy("car-list")

class UserList(ListView):
    model = User
    paginate_by = 20

class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("user-list")

class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("user-list")

class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy("user-list")

class CarPhotoCreate(CreateView):
    model = CarPhoto
    form_class = CarPhotoForm

    def form_valid(self, form):
        form.instance.car_id = self.kwargs["pk"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.car.get_absolute_url() if hasattr(self.object.car, "get_absolute_url") else reverse_lazy("car-detail", args=[self.object.car_id])
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('car-list')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

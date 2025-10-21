from django.shortcuts import redirect, render
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
import requests
from django.contrib import messages
from django.core.files.base import ContentFile
from .services import fetch_retail_photo_urls_by_vin
from .models import Profile
from .forms import ProfileForm, UserAccountForm

class Home(LoginView):
    template_name = 'home.html'

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'autolot/profile_detail.html'

    def get_object(self, queryset=None):
        return self.request.user.profile
    
class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'autolot/profile_form.html'
    success_url = reverse_lazy('profile-detail')

    def get_object(self, queryset=None):
        return self.request.user.profile
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserAccountForm(request.POST, instance=request.user)
        form = self.get_form()
        user_form.save()
        return self.form_valid(form)

class CarList(ListView):
    model = Car
    template_name = 'autolot/car_list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')

        if q:
            qs = qs.filter(Q(make__icontains=q) | Q(model__icontains=q) | Q(vin__icontains=q))
        if status:
            qs = qs.filter(status=status)
        return qs

class CarDetail(DetailView):
    model = Car
    template_name = 'autolot/car_detail.html'

class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'autolot/form.html'
    success_url = reverse_lazy('car-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

class CarUpdate(UpdateView):
    model = Car
    form_class = CarForm
    template_name = "autolot/form.html"
    success_url = reverse_lazy('car-list')

class CarDelete(DeleteView):
    model = Car
    success_url = reverse_lazy('car-list')

class UserList(ListView):
    model = User
    paginate_by = 20

class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('user-list')

class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('user-list')

class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user-list')

class CarPhotoCreate(CreateView):
    model = CarPhoto
    form_class = CarPhotoForm

    def form_valid(self, form):
        form.instance.car_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('import_api') == '1':
            car = Car.objects.get(pk=self.kwargs['pk'])
            try:
                urls = fetch_retail_photo_urls_by_vin(car.vin)
                if not urls:
                    messages.error(request, 'No photo available.')
                    return redirect('car-detail', pk=car.pk)

                u = urls[0]
                resp = requests.get(u, timeout=15)
                resp.raise_for_status()
                filename = (u.split('/')[-1].split('?')[0]) or f"{car.vin}.jpg"

                photo = CarPhoto(car=car)
                photo.image.save(filename, ContentFile(resp.content), save=True)
                messages.success(request, 'Imported default.')
            except Exception as e:
                messages.error(request, f"Import failed: {e}")
            return redirect('car-detail', pk=car.pk)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('car-detail', args=[self.kwargs["pk"]])
    
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

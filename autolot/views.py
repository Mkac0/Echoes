from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Car, CustomerLead, CarPhoto
from .forms import CarForm, CustomerLeadForm, CarPhotoForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests
from django.contrib import messages
from django.core.files.base import ContentFile
from .services import fetch_retail_photo_urls_by_vin
from .models import Profile
from .forms import ProfileForm, UserAccountForm, CarPhotoEditForm

class Home(LoginView):
    template_name = 'home.html'

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'autolot/profile_detail.html'
    def get_object(self, queryset=None):
        return self.request.user.profile

class ProfilePublicDetail(DetailView):
    model = Profile
    template_name = 'autolot/profile_detail.html'

class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'autolot/profile_form.html'
    success_url = reverse_lazy('profile-detail')
    def get_object(self, queryset=None):
        return self.request.user.profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['user_form'] = UserAccountForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserAccountForm(instance=self.request.user)
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserAccountForm(request.POST, instance=request.user)
        form = self.get_form()
        if form.is_valid() and user_form.is_valid():
            user_form.save()
            return self.form_valid(form)
        context = self.get_context_data(form=form)
        context['user_form'] = user_form
        return self.render_to_response(context)

class CarList(ListView):
    model = Car
    template_name = 'autolot/car_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query') or ''
        status = self.request.GET.get('status')
        if query:
            queryset = queryset.filter(vin__icontains=query)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

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

class CarUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = "autolot/form.html"
    success_url = reverse_lazy('car-list')
    def test_func(self):
        car = self.get_object()
        return car.owner == self.request.user

class CarDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('car-list')
    def test_func(self):
        car = self.get_object()
        return car.owner == self.request.user

class CustomerLeadList(ListView):
    model = CustomerLead
    paginate_by = 20

class CustomerLeadCreate(LoginRequiredMixin, CreateView):
    model = CustomerLead
    form_class = CustomerLeadForm
    success_url = reverse_lazy('customerlead-list')

class CustomerLeadUpdate(UpdateView):
    model = CustomerLead
    form_class = CustomerLeadForm
    success_url = reverse_lazy('customerlead-list')

class CustomerLeadDelete(DeleteView):
    model = CustomerLead
    success_url = reverse_lazy('customerlead-list')

class CarPhotoCreate(CreateView):
    model = CarPhoto
    form_class = CarPhotoForm
    def form_valid(self, form):
        form.instance.car_id = self.kwargs['pk']
        return super().form_valid(form)
    def post(self, request, *args, **kwargs):
        if request.POST.get('import_api') == '1':
            try:
                car = Car.objects.get(pk=self.kwargs['pk'])
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
                messages.success(request)
            except requests.exceptions.RequestException as error:
                messages.error(request, f"{error}")
            return redirect('car-detail', pk=self.kwargs['pk'])
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
            error_message = 'Invalid - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

class CarPhotoUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CarPhoto
    form_class = CarPhotoEditForm
    template_name = "autolot/carphoto_form.html"
    def test_func(self):
        return self.get_object().car.owner == self.request.user
    def get_success_url(self):
        return reverse("car-detail", args=[self.object.car_id])

class CarPhotoDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CarPhoto
    template_name = "autolot/carphoto_confirm_delete.html"
    def test_func(self):
        return self.get_object().car.owner == self.request.user
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        storage, path = obj.image.storage, obj.image.name
        response = super().delete(request, *args, **kwargs)
        if path:
            storage.delete(path)
        return response
    def get_success_url(self):
        return reverse("car-detail", args=[self.object.car_id])

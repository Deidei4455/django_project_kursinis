from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import check_password
from .models import Gamintojas, Modelis, Klientas, Car, Paslaugos, Uzsakymas, PaslaugaUzsakymas, User
from .forms import UzsakymasReviewForm, ProfileUpdateForm, UserUpdateForm, UserUzsakymasCreateForm


# Create your views here.

def index(request):
    num_paslaugos = Paslaugos.objects.count()
    num_uzsakymas = Uzsakymas.objects.count()
    num_paslauga_uzsakymas = PaslaugaUzsakymas.objects.count()
    num_car = Car.objects.count()
    num_klientas = Klientas.objects.count()
    num_modelis = Modelis.objects.count()
    num_gamintojas = Gamintojas.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_paslaugos': num_paslaugos,
        'num_uzsakymas': num_uzsakymas,
        'num_paslauga_uzsakymas': num_paslauga_uzsakymas,
        'num_car': num_car,
        'num_klientas': num_klientas,
        'num_modelis': num_modelis,
        'num_gamintojas': num_gamintojas,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def get_cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 8)
    page_number = request.GET.get('page')

    paged_cars = paginator.get_page(page_number)
    return render(request, 'cars.html', context={'cars': paged_cars})


def get_one_car(request, car_id):
    one_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', context={'one_car': one_car})


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymas_list'
    template_name = 'uzsakymai.html'
    paginate_by = 6


class UzsakymasDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Uzsakymas
    context_object_name = 'uzsakymas'
    template_name = 'uzsakymas.html'
    form_class = UzsakymasReviewForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.uzsakymas_object = self.get_object()
        form.instance.uzsakymas = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.uzsakymas_object.id})


def order_with_status(request, status_s):
    uzsakymai = Uzsakymas.objects.filter(status=status_s)
    return render(request, 'orderstatus.html', context={'uzsakymai': uzsakymai})


def search(request):
    query_text = request.GET.get('search_text')
    search_results = Car.objects.filter(Q(modelis__modelis__icontains=query_text) |
                                        Q(autonr__icontains=query_text) |
                                        Q(klientas__f_name__icontains=query_text) |
                                        Q(modelis__gamintojas__gamintojas__icontains=query_text))

    return render(request, 'search_res.html',
                  context={'query_text': query_text,
                           'search_results': search_results})


class KlientasListView(generic.ListView):
    model = Klientas
    context_object_name = 'klientas_list'
    template_name = 'klientai.html'
    paginate_by = 6


# class KlientasDetailView(generic.DetailView):
#     model = Klientas
#     context_object_name = 'klientas'
#     template_name = 'klientas.html'


def get_klientas(request, klientas_id):
    one_klientas = get_object_or_404(Klientas, pk=klientas_id)
    client_cars = Car.objects.filter(klientas=one_klientas)
    context = {'one_klientas': one_klientas,
               'client_cars': client_cars}
    return render(request, 'klientas.html', context=context)


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymas_list'
    template_name = 'myorders.html'

    def get_queryset(self):
        return Uzsakymas.objects.filter(uzsakovas=self.request.user)


@csrf_protect
def register_user(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not check_password(password):
            messages.error(request, 'Password must be longer than 5 symbols')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"User with {username} already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, f"{email} is already taken")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)

        messages.info(request, f"User {username} has been registered")
        return redirect('login')


@login_required()
def get_user_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.info(request, 'Profile updated')
        else:
            messages.error(request, 'Profile not updated')
        return redirect('user-profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', context={
        'p_form': p_form,
        'u_form': u_form
    })


class UzsakymasByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    form_class = UserUzsakymasCreateForm
    template_name = 'user_uzsakymas_form.html'
    success_url = '/autoservisas/myorders'

    def form_valid(self, form):
        form.instance.uzsakovas = self.request.user
        form.instance.status = 'a'
        return super().form_valid(form)


class UzsakymasByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    form_class = UserUzsakymasCreateForm
    template_name = 'user_uzsakymas_form.html'
    success_url = '/autoservisas/myorders'

    def form_valid(self, form):
        form.instance.uzsakovas = self.request.user
        form.instance.status = 'a'
        return super().form_valid(form)

    def test_func(self):
        uzsakymas_object = self.get_object()
        return uzsakymas_object.uzsakovas == self.request.user


class UzsakymasByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    template_name = 'user_uzsakymas_delete.html'
    success_url = '/autoservisas/myorders'
    context_object_name = 'uzsakymas'

    def test_func(self):
        uzsakymas_object = self.get_object()
        return uzsakymas_object.uzsakovas == self.request.user

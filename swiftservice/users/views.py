from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse,reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import CustomerSignupForm, SupportStaffSignupForm, ServiceProviderSignupForm, TaskForm
from .models import Customer, ServiceProvider, SupportStaff
User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()



class CustomerSignupView(CreateView):
    template_name = 'account/signup.html'
    form_class = CustomerSignupForm
    success_url = reverse_lazy('home')  # Replace with your success URL

    def form_valid(self, form):
        user = form.save(self.request)
        user.is_customer = True
        user.save()
        phone_number = form.cleaned_data['phone_number']
        address = form.cleaned_data['address']
        preferences = form.cleaned_data['preferences']
       
        # Create Customer instance
        Customer.objects.create(user=user, phone_number=phone_number, address=address, preferences=preferences)
        
        return super().form_valid(form)


class SupportStaffSignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = SupportStaffSignupForm
    success_url = _('home')  # Replace with your success URL

    def form_valid(self, form):
        user = form.save(self.request)
        user.is_support_staff = True
        user.save()
        job_title = form.cleaned_data['job_title']
        department = form.cleaned_data['department']
        skills = form.cleaned_data['skills']
        schedule = form.cleaned_data['schedule']
        
        # Create SupportStaff instance
        SupportStaff.objects.create(user=user, job_title=job_title, department=department,
                                    skills=skills, schedule=schedule)
        
        return super().form_valid(form)

class ServiceProviderSignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = ServiceProviderSignupForm
    success_url = _('uses:detail')  # Replace with your success URL

    def form_valid(self, form):
        user = form.save(self.request)
        user.is_service_provider = True
        user.save()
        phone_number = form.cleaned_data['phone_number']
        address = form.cleaned_data['address']
        skills = form.cleaned_data['skills']
        service_area = form.cleaned_data['service_area']
        availability = form.cleaned_data['availability']
        
        # Create ServiceProvider instance
        ServiceProvider.objects.create(user=user, phone_number=phone_number, address=address,
                                        skills=skills, service_area=service_area,
                                        availability=availability)
        
        return super().form_valid(form)



def home(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            if not request.user.is_authenticated:
                # Create a visitor user instance
                visitor_user, created = User.objects.get_or_create(
                    email='visitor@gmail.com',
                    defaults={'password': User.objects.make_random_password()}
                )
                if created:
                    customer = Customer.objects.create(
                        user=visitor_user,
                        phone_number='080',  # Set your default value
                        address='default Visitor Address',  # Set your default value
                        preferences='cash',  # Set your default value
                    )
                else:
                    customer = Customer.objects.get(user=visitor_user)
                task = task_form.save(commit=False)
                task.customer = customer
            else:
                task = task_form.save(commit=False)
                task.customer = request.user.customer

            task.save()
            return redirect('home')
    else:
        task_form = TaskForm()
    return render(request, 'pages/home.html', {'task_form': task_form})


# def handle_task_dahboard(request):
#intedn to use a diffrerent redirect fo rthis view in dashboad
# import json
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse,reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from allauth.account.views import SignupView
from .forms import CustomerSignupForm, SupportStaffSignupForm, ServiceProviderSignupForm, ServiceForm, RestaurantForm, DishForm
from .models import Customer, ServiceProvider, SupportStaff, Pickup, Delivery, Task, Restaurant
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

def support_staff_signup(request):
    if request.method == 'POST':
        form = SupportStaffSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            user.is_support_staff = True
            user.save()
            job_title = form.cleaned_data['job_title']
            department = form.cleaned_data['department']
            skills = form.cleaned_data['skills']
            schedule = form.cleaned_data['schedule']
            
            # Create SupportStaff instance
            SupportStaff.objects.create(user=user, job_title=job_title, department=department,
                                        skills=skills, schedule=schedule)
            
            return redirect('users:detail', pk=user.pk)  # Replace 'home' with your success URL name
    else:
        form = SupportStaffSignupForm()
    
    return render(request, 'account/signup2.html', {'form': form})

def service_provider_signup(request):
    if request.method == 'POST':
        form = ServiceProviderSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            user.is_service_provider = True
            user.save()
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            service = form.cleaned_data['service']
            service_area = form.cleaned_data['service_area']
            availability = form.cleaned_data['availability']
            
            # Create ServiceProvider instance
            ServiceProvider.objects.create(user=user, phone_number=phone_number, address=address,
                                            service=service, service_area=service_area,
                                            availability=availability)
            
            return redirect('users:detail', pk=user.pk )  # Replace with your actual success URL
    else:
        form = ServiceProviderSignupForm()
    
    return render(request, 'account/signup3.html', {'form': form})

def home(request):
    # if request.method == 'POST':
    #     task_form = TaskForm(request.POST)
    #     if task_form.is_valid():
    #         if not request.user.is_authenticated:
    #             # Create a visitor user instance
    #             visitor_user, created = User.objects.get_or_create(
    #                 email='visitor@gmail.com',
    #                 defaults={'password': User.objects.make_random_password()}
    #             )
    #             if created:
    #                 customer = Customer.objects.create(
    #                     user=visitor_user,
    #                     phone_number='080',  # Set your default value
    #                     address='default Visitor Address',  # Set your default value
    #                     preferences='cash',  # Set your default value
    #                 )
    #             else:
    #                 customer = Customer.objects.get(user=visitor_user)
    #             task = task_form.save(commit=False)
    #             task.customer = customer
    #         else:
    #             task = task_form.save(commit=False)
    #             task.customer = request.user.customer

    #         task.save()
    #         return redirect('home')
    # else:
    # task_form = TaskForm()
    form = ServiceForm()

    return render(request, 'pages/home.html', {'form': form, 'restaurants': Restaurant.objects.all()})


# def handle_task_dahboard(request):
#intedn to use a diffrerent redirect fo rthis view in dashboad



def submit_form(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            task_type = form.cleaned_data['task_type']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            pickup_location = form.cleaned_data['pickup_location']
            pickup_datetime = form.cleaned_data['pickup_datetime']
            delivery_location = form.cleaned_data['delivery_location']
            delivery_datetime = form.cleaned_data['delivery_datetime']
            delivery_category = form.cleaned_data['delivery_category']

        if not request.user.is_authenticated:
            # Create a visitor user instance
            print('not authenticated...................')
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
        else:
            customer = request.user.customer
        
        # Create Task, Pickup, and Delivery objects as needed
        
        task = Task.objects.create(
            task_type=task_type,
            title=title,
            description=description,
            due_date=due_date,
            customer=customer
        )
        if task_type == 'pickup_delivery':
            pickup = Pickup.objects.create(
                pickup_location=pickup_location,
                pickup_datetime=pickup_datetime,
            )
            delivery = Delivery.objects.create(
                delivery_location=delivery_location,
                delivery_datetime=delivery_datetime,
                category=delivery_category,
            )
            task.pickup = pickup
            task.delivery = delivery

        # Save the Task object
        task.save()
    else:
        form = ServiceForm()

        # Redirect to the home page (change 'home' to the actual URL name of your home page)
        return redirect('home')

    # Handle GET requests (if needed)
    return render(request, 'pages/home.html')


# resturant

def add_restaurant_view(request):
    user_restaurants = Restaurant.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            new_restaurant = form.save(commit=False)
            new_restaurant.owner = request.user
            new_restaurant.save()
            return redirect('users:add_restaurant')
    else:
        form = RestaurantForm()
        dish_form = DishForm()
    return render(request, 'restaurant/add.html', {'form': form, 'dish_form': dish_form, 'restaurants': user_restaurants})


def add_dish_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    if request.method == 'POST':
        dish_form = DishForm(request.POST, request.FILES)
        if dish_form.is_valid():
            new_dish = dish_form.save(commit=False)
            new_dish.restaurant = restaurant
            new_dish.save()

            response_data = {'message': 'Dish added successfully'}
            return JsonResponse(response_data)

    return redirect('users:add_restaurant')  # Redirect to a suitable page if needed


def restaurant_dishes_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    dishes = restaurant.dish_set.all()
    
    return render(request, 'restaurant/dishes.html', {'restaurant': restaurant, 'dishes': dishes})


# Restaurant users
def restaurant_all(request):
    return render(request, 'restaurant/restaurant_list.html', {'restaurants': Restaurant.objects.all()})

def restaurant_dishes_all(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    dishes = restaurant.dish_set.all()
    return render(request, 'restaurant/dishes_all.html', {'restaurant': restaurant, 'dishes': dishes})
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Customer, SupportStaff, ServiceProvider, Task, Restaurant, Dish

User = get_user_model()

class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


PAYMENT_PREFERENCES_CHOICES = (
    ('credit_card', 'Credit Card'),
    ('cash', 'Cash'),
    ('offline_payment', 'Offline Payment'),
    ('partial_payment', 'Partial Payments'),
)


class CustomerSignupForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField()
    # payment_information = forms.CharField(widget=forms.Textarea)
    preferences = forms.MultipleChoiceField(choices=PAYMENT_PREFERENCES_CHOICES, widget=forms.CheckboxSelectMultiple)
    # notifications = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class SupportStaffSignupForm(SignupForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    job_title = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    skills = forms.CharField(widget=forms.Textarea)
    schedule = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class ServiceProviderSignupForm(SignupForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100)
    service = forms.CharField(max_length=200)
    service_area = forms.CharField(max_length=100)
    availability = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


# class TaskForm(forms.ModelForm):
#     """Form definition for Task."""

#     class Meta:
#         """Meta definition for Taskform."""

#         model = Task
#         fields = (
#             'task_type',
#             'title',
#             'description',
#             'due_date'
#             )
        
class ServiceForm(forms.Form):
    TASK_TYPES = [
        ('pickup_delivery', 'Pickup and Delivery'),
        ('cleaning', 'Cleaning Service (Coming Soon)'),
        ('task_delegation', 'Task Delegation (Coming Soon)'),
    ]

    task_type = forms.ChoiceField(choices=TASK_TYPES, widget=forms.Select(attrs={'onchange': 'handleTaskTypeChange();'}))
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateTimeField()
    pickup_location = forms.CharField(max_length=100, required=False)
    pickup_datetime = forms.DateTimeField(required=False)
    delivery_location = forms.CharField(max_length=100, required=False)
    delivery_datetime = forms.DateTimeField(required=False)
    delivery_category = forms.ChoiceField(
        choices=[('shoes', 'Shoes'), ('electronics', 'Electronics'), ('jewelry', 'Jewelry')],
        required=False,
    )


# resturant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'image']
        

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image']
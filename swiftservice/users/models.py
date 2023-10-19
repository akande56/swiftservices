from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from swiftservice.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for swiftservice.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    is_customer = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)
    is_support_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})



class SupportStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = CharField(max_length=100)
    department = CharField(max_length=100)
    skills = models.CharField(max_length=100)
    schedule = CharField(max_length=200)
    
    def __str__(self):
        return str(self.user.email)

PAYMENT_PREFERENCES_CHOICES = (
    ('credit_card', 'Credit Card'),
    ('cash', 'Cash'),
    ('offline_payment', 'Offline Payment'),
    ('partial_payment', 'Partial Payments'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = CharField(max_length=15)
    address = models.CharField(max_length=100)
    # payment_information = models.TextField()
    preferences = models.CharField(max_length=400, choices=PAYMENT_PREFERENCES_CHOICES)
    # notifications = models.TextField() let use inbox instead

    def __str__(self):
        return str(self.user.email)


class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = CharField(max_length=15)
    address = models.CharField(max_length=100)
    service = models.CharField(max_length=200)
    service_area = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.email)


class Pickup(models.Model):
    pickup_location = models.CharField(max_length=100)
    pickup_datetime = models.DateTimeField()
    additional_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Pickup  at {self.pickup_datetime}"


class Delivery(models.Model):
    CATEGORY_CHOICES = (
        ('shoes', 'Shoes'),
        ('electronics', 'Electronics'),
        ('jewelry', 'Jewelry'),
        # Add more category options as needed
    )
    delivery_location = models.CharField(max_length=100)
    delivery_datetime = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Delivery  at {self.delivery_datetime}"


class Task(models.Model):
    TASK_TYPES = (
        ('pickup_delivery', 'Pickup and Delivery'),
        ('cleaning', 'Cleaning Service (Coming Soon)'),
        ('task_delegation', 'Task Delegation (Coming Soon)'),
    )
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='created_tasks')
    assignee = models.ForeignKey(SupportStaff, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    pickup = models.OneToOneField(Pickup, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_pickup')
    delivery = models.OneToOneField(Delivery, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_delivery')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(SupportStaff, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on task: {self.task.title}"


class TaskAttachment(models.Model)  :
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    attachment = models.FileField(upload_to='task_attachments/')
    uploaded_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for task: {self.task.title}"


# <script async src="https://whatsform.com/launcher.js" id="wf-widget" data-id="MY_kW1" data-message="Message on WhatsApp" ></script>

# Define a model for Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)  # Add this field
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

# Define a model for Dish Category (e.g., Appetizer, Main Course, Dessert)


# Define a model for Dish
class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
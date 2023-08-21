from django.urls import path

from swiftservice.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    CustomerSignupView,
    SupportStaffSignupView,
    ServiceProviderSignupView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path('signup/customer/', CustomerSignupView.as_view(), name='customer_signup'),
    path('signup/support_staff/', SupportStaffSignupView.as_view(), name='support_staff_signup'),
    path('signup/service_provider/', ServiceProviderSignupView.as_view(), name='service_provider_signup'),
]
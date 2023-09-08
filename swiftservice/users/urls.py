from django.urls import path

from swiftservice.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    CustomerSignupView,
    # SupportStaffSignupView,
    support_staff_signup,
    service_provider_signup,
    submit_form,
    add_restaurant_view,
    add_dish_view,
    restaurant_dishes_view,
    restaurant_all,
    restaurant_dishes_all,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path('signup/customer/', CustomerSignupView.as_view(), name='customer_signup'),
    path('signup/support_staff/', support_staff_signup  , name='support_staff_signup'),
    path('signup/service_provider/', service_provider_signup, name='service_provider_signup'),
    path('submit_form/', submit_form, name='submit_form'),
    path('resturant', add_restaurant_view, name='add_restaurant'),
    path('resturant/add_dish_ajax/<int:restaurant_id>', add_dish_view, name='add_dish'),
    path('restaurant/<int:restaurant_id>/dishes/', restaurant_dishes_view, name='restaurant_dishes'),
    path('restaurant/all', restaurant_all, name='restaurant_list'),
    path('restaurant/<int:restaurant_id>/dishes/all', restaurant_dishes_all, name='restaurant_dishes_all'),
]

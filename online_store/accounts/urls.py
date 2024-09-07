from django.urls import path
from .views import sign_up, login_view, role_based_home

urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', login_view, name='login'),
    path('home/', role_based_home, name='role_based_home'),
]

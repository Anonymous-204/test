from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="index"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('api/register/', views.register_api),
    path('api/login/', views.login_api),
    path('friends/',views.friends_view, name="friends")
]

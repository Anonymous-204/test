from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="index"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('changepassword/',views.changepassword),
    path('api/register/', views.register_api),
    path('api/login/', views.login_api),
    path('api/changepassword/', views.change_password_api),
    path("api/logout/", views.logout_api),
    path('friends/',views.friends_view, name="friends"),
    path('add-task/', views.add_task_view, name='add_task'),
    path('archive/', views.archive_view, name='archive'),
    path('complete-task/<int:task_id>/', views.complete_task_view, name='complete_task'),
    path('delete-task/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path("delete-archived-task/<int:task_id>/", views.delete_archived_task, name="delete_archived_task"),
]

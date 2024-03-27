from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.user_profile, name="user_profile"),
    path('account/', views.user_account, name="account"),
    path("edit_account/", views.edit_account, name="edit_account"),
    path("create_skill/", views.create_skill, name="create_skill"),
    path("update_skill/<str:pk>/", views.update_skill, name="update_skill"),
    path("delete_skill/<str:pk>/", views.delete_skill, name="delete_skill"),
]
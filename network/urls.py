
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    # API routes
    path("follow/", views.follow),
    path("edit/<int:post_id>", views.edit),
    path("<int:user_id>/edit/<int:post_id>", views.edit_from_profile),
    path("like/<int:post_id>", views.like),
    path("toggle_visibility/<int:post_id>", views.toggle_visibility),
    
]

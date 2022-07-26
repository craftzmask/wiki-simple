from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_entry, name="view_entry"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit_entry"),
    path("search", views.search, name="search"),
    path("create", views.create_entry, name="create_entry"),
    path("random", views.random_page, name="random_page")
]

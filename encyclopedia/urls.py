from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_entry, name="get_entry"),
    path("search", views.search, name="search"),
    path("create", views.create_entry, name="create_entry")
]

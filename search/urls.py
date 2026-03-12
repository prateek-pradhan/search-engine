from django.urls import path
from . import views

urlpatterns = [
    path("<str:title>/", views.basic_search, name="basic_search"),
    path("wiki/<int:id>/", views.get_wiki, name="get_wiki"),
]
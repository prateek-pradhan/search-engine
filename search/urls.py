from django.urls import path
from . import views

urlpatterns = [
    path("", views.tokenized_query, name="tokenized_query"),
    path("wiki/<int:id>/", views.get_wiki, name="get_wiki"),
]
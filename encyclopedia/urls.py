from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("?q=", views.search, name="search"), also working, but url looks %3Fq=?q=, wiki is better
    path("wiki/", views.search, name="search"),
    path("rand/wiki", views.rand, name="rand"),
    path("wiki/<str:name>", views.article, name="article"),
    path("wiki/wiki/<str:name>", views.article, name="article1"),
    path("newp/", views.newp, name="newpage"),
    path("newp/saving/", views.save, name="save"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("wiki/edit/<str:name>", views.edit, name="edit1"),
    path("edit/saving/", views.edsave, name="edsave"),
    path("wiki/edit/", views.edsave, name="edsave1"),
    path("newp/edit/<str:name>", views.edit, name="edit2"),
    path("edit/edit/<str:name>", views.edit, name="edit3"),
    # path("?q=<str:name>", views.article, name="search"), this requires 2nd argument for search, not working
    # path("", views.index, name="search"), not working, same path as index, index processed
]

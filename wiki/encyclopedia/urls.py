from django.urls import path

from . import views,util

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>",views.entry_view,name="entry"),
    path("search/",views.search,name="search"),
    path("new_page/",views.new_page,name="new_page"),
    path("new_entry/",views.new_entry,name="new_entry"),
    
    path("edit/",views.edit_py,name="edit"),
    path("random/",views.random_page,name="random"),
]

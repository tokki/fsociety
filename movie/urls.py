from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('movie/', views.list, name='list'),
    path('tv/', views.tv_list, name='tvlist'),
    path('seed/<int:movie_id>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('people/', views.people, name='people'),
]

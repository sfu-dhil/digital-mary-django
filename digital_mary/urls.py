from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about', views.AboutView.as_view(), name='about'),
    path('items', views.ItemsView.as_view(), name='items'),
    path('items/<int:pk>', views.ItemView.as_view(), name='item'),
]
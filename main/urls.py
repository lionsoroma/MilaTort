from django.urls import path, include
from details import views as views2
from main import views

urlpatterns = [
    path('', views.main, name='main'),
    path('details/tab/<str:slug>/<int:active_fancy_tab_id>/', views2.details_product, name='details_product'),
]

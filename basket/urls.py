from django.urls import path, include
from basket import views


urlpatterns = [

    path('basket_finish/', views.basket_finish, name='basket_finish'),
    path('', views.cities_streets, name='cities_streets'),
    path('congratulations/', views.basket_table, name='basket_table'),
]



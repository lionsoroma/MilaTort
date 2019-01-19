from django.urls import path, include
from details import views


urlpatterns = [
    path('details/<str:slug>/<int:order_id>/', views.details_product, name='details_product'),
    path('details/<str:slug>/', views.details_product, name='details_product'),
    path('send_commit/', views.send_commit, name='send_commit'),
]



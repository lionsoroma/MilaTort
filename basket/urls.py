from django.urls import path, include
from basket import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('basket_finish/', views.basket_finish, name='basket_finish'),
    path('', views.cities_streets, name='cities_streets'),
    path('congratulations/', views.basket_table, name='basket_table'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


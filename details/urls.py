from django.urls import path, include
from details import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('details/<str:slug>/<int:order_id>/', views.details_product, name='details_product'),
    path('details/<str:slug>/', views.details_product, name='details_product'),
    path('send_commit/', views.send_commit, name='send_commit'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


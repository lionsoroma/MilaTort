from django.urls import path, include
from details import views as views2
from main import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.main, name='main'),
    path('details/tab/<str:slug>/<int:active_fancy_tab_id>/', views2.details_product, name='details_product'),

]

if settings.DEBUG is True:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
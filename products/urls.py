from django.urls import path, include
from products import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('orders.urls')),
    path('products/<str:slug>', views.list_product, name='list_product'),
    path('', include('details.urls')),
    path('', include('basket.urls')),
    path('login_logout/', views.login_logout, name='login_logout'),
    path('password_reset_tel/', views.password_reset_via_tel, name='password_reset_via_tel'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

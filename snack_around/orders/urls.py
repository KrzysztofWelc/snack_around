from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('product', views.ProductView.as_view(), name='product'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product'),
]

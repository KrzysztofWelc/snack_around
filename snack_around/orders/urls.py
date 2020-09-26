from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('product', views.ProductView.as_view(), name='product'),
    path('product/list', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product'),
]

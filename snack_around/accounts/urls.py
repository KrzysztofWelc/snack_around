from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register', views.register_view, name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('restaurants', views.ListRestaurantsView.as_view(), name='restaurants'),
    path('restaurant/<int:pk>/', views.UserView.as_view(), name='restaurant'),
    path('image', views.ImageView.as_view(), name='image'),
    path('image/<int:pk>/', views.ImageView.as_view(), name='image'),
]

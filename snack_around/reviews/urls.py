from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'reviews'
urlpatterns = [
    path('', views.ReviewView.as_view()),
    path('list/', views.ReviewListView.as_view()),
    path('<int:pk>/', views.ReviewView.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
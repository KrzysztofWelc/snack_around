from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', 'frontend')),
    path('api/account/', include('accounts.urls', 'accounts')),
    path('api/reviews/', include('reviews.urls', 'reviews')),
]

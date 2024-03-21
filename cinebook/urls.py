from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', include('movies.urls')),
    path('admin/', admin.site.urls),
    path("blog/", include('blog.urls')),
    path('users/', include('users.urls')),
    path('cinemas/', include('cinemas.urls')),
    path('showtimes/', include('showtimes.urls')),
    path('screeningrooms/', include('screeningrooms.urls')),
    path('bookings/', include('bookings.urls')),
    # JWT Auth paths
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls', namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('password-reset/', include('password_reset.urls')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('notice/', include('notice.urls', namespace='notice')),
    path('accounts/', include('allauth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
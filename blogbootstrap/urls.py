from django.urls import include, re_path, path
from django.contrib import admin
import django.contrib.auth.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^blog/', include('blog.urls')),
    re_path(r'', include('carousel.urls')),
    re_path(r'^tempurls/', include('tempurls.urls')),
    re_path(r'^soundtracks/', include('soundtracks.urls')),
    re_path(r'^speaker/', include('speaker.urls')),
    re_path(r'^bredbot/', include('bredbot.urls')),
    re_path(r'^uprofile/', include('uprofile.urls')),
    re_path(r'^accounts/login/$', LoginView.as_view(), name='login'),
    re_path(r'^accounts/logout/$', LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
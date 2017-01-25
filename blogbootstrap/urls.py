from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views
#from django.conf import settings
#from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
    url(r'', include('carousel.urls')),
    url(r'^tempurls/', include('tempurls.urls')),
    url(r'^soundtracks/', include('soundtracks.urls')),
    url(r'^speaker/', include('speaker.urls')),
    url(r'^bredbot/', include('bredbot.urls')),
    url(r'^uprofile/', include('uprofile.urls')),
    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^i18n/', include('django.conf.urls.i18n')),

] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
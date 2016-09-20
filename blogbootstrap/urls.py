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
    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

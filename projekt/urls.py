    # Examples:
    # url(r'^$', 'projekt.views.home', name='home'),
    # url(r'^projekt/', include('projekt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
from django.conf.urls import *
from django.conf import settings
from aplikacja.views import strona_glowna
from aplikacja.views import podstrona
from zbieracz.views import zasysamy
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^index/$', strona_glowna),
    (r'^zasysamy/$', zasysamy),
    (r'^$', strona_glowna),
    (r'^admin/', admin.site.urls),
    # (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # # (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^image/(?P<id_obrazka>\d+)', podstrona),
)

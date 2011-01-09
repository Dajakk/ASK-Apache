from django.conf.urls.defaults import *
from ASK_Apache.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ASK_Apache/', include('ASK_Apache.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^hello/$', hello),
    (r'^datetime/$', current_datetime),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^test/$', show_virtual_hosts),
    (r'^editVirtualHost/(\d*)/$', edit_virtual_host),
    (r'^editNode/(\d*)/$', edit_node),
)

from django.conf.urls import include, url
from django.contrib import admin

import apis.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^register/',apis.views.register,name='register'),
    url(r'^fetch_details/',apis.views.fetch,name='fetch'),
    # url(r'^register/',apis.views.register_node,name='register'),   #uncomment them for neo4j
    # url(r'^fetch_details/',apis.views.fetch_node,name='fetch'),
    url(r'^admin/', include(admin.site.urls)),
]

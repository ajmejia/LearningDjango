from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'pollsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #-----------------------------------------------------------
    #- the url function takes te following arguments:
    #-    * regex: regular expression to map againts defined
    #-             urls.
    #-    * view: the to which will be called upon the match.
    #-    + kwargs: arguments passed to the target view.
    #-    + name: name usde to reference across templates.
    #-----------------------------------------------------------

    url(r'^polls/', include('polls.urls')),                #- The ^polls/ patterns are handled by
                                                           #- the polls.urls.
    url(r'^admin/', include(admin.site.urls)),
]

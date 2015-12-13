from django.conf.urls import include, url
from django.contrib import admin

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

urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace='polls')),         #- The ^polls/ patterns are handled by polls.urls.
                                                                       #- The namespace is used to differenciate between
                                                                       #- views with the same name but different app.
    url(r'^admin/', include(admin.site.urls)),
]

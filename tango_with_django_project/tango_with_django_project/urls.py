from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

#Create a new class that redirects the user to index page, if successful on login
class MyRegistrationView(RegistrationView):
	def get_success_url(self, request, user):
		return '/rango/'

urlpatterns = [
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),
	url(r'^rango/', include('rango.urls')),
	url(r'^accounts/', include('registration.backends.simple.urls')),
)
'''

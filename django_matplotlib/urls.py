from django.conf.urls.defaults import *

"""
URL usage:

plot/<plot_type>.<format>

for example:

    plot/pie.png

will output output a pie chart in png format.

If your web server is configured to have a differnt handle on image extensions you may use an alternative representation instead.

"""
urlpatterns = patterns('',
    url(r'^plot/(\w+)\.(\w+)$', 'django_matplotlib.views.plot_view',  name="pyplot-view"),
    #url(r'^plot/(\w+)-(\w+)$', 'django_matplotlib.views.plot_view',  name="pyplot-view-alternative"),
)

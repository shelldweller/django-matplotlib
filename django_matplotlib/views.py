import django_matplotlib.settings as mpl_settings
from django_matplotlib.mapping import extract_kwargs, KNOWN_CHART_LIST, str2num, str2bool
import matplotlib

from django.http import HttpResponse, HttpResponseNotFound

matplotlib.use(mpl_settings.BACKEND)

from matplotlib import pyplot


def plot_view(request, plot_type, format="png"):
    """
    Universal view for generating plots. Valid plot types are defined in
    `django_matplotlib.mapping.KNOWN_CHART_LIST`
    """
    
    # initial validation
    try:
        content_type = mpl_settings.FORMATS[format]
    except KeyError:
        return HttpResponseNotFound("Unknown output format: '%s'" % format)    
    if plot_type not in KNOWN_CHART_LIST:
        return HttpResponseNotFound("Unknown plot type: '%s'" % plot_type)
    
    # prepare plot
    fig = pyplot.figure(**extract_kwargs("figure", request.GET))
    
    # FIXME: need to be able to set other things like:
    #plt.ylabel('Scores')
    #plt.title('Scores by group and gender')
    #plt.xticks(ind+width/2., ('G1', 'G2', 'G3', 'G4', 'G5') )
    #plt.yticks(np.arange(0,81,10))
    #plt.legend( (p1[0], p2[0]), ('Men', 'Women') )
    
    ax = fig.add_subplot(111) # FIXME: what's 111? And why do we need subplot?
    plot_object = getattr(ax, plot_type) # we shouldn't really get AttributeError here
    
    # initialize args and draw plot
    kwargs = extract_kwargs(plot_type, request.GET)
    # TODO: plot_object(**kwargs) error handling
    # TypeError if not enough arguments
    # AssertionError if arguments don't make sense
    plot_object(**kwargs)
    
    # set plot properties
    if "ylabel" in request.GET:
        ax.set_ylabel(request.GET.get("ylabel"))
    if "xlabel" in request.GET:
        ax.set_xlabel(request.GET.get("xlabel"))
    if "title" in request.GET:
        ax.set_title(request.GET.get("title"))
    if "xtickoffset" in request.GET: # FIXME: xtickoffset is probably a misfeature
        offset = str2num(request.GET.get("xtickoffset"))
        xticks = ax.get_xticks()
        ax.set_xticks(map(lambda x:x+offset, xticks))
        ax.set_xticklabels(xticks)
    if "legend" in request.GET and str2bool(request.GET.get("legend")):
        ax.legend()
    if str2bool(request.GET.get("grid", "0")):
        ax.grid()
    # set_xticklabels
    # 
    
    # prepare and output HTTP response
    response=HttpResponse(content_type=content_type)
    fig.savefig(response, format=format)    
    return response

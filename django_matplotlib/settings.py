from django.conf import settings
import os

# keys are format names (extensions) and values are corresponding content-types
DEFAULT_FORMATS = {
    "png" : "image/png",
    "pdf" : "application/pdf",
    "ps"  : "application/postscript",
    "eps" : "application/postscript",
    "svg" : "image/svg+xml"
}
# configdir default to $HOME/.matplotlib which is not particularly useful when running from web server
DEFAULT_MPLCONFIGDIR = '/tmp' # FIXME: this is probably a poor default choice

BACKEND = getattr(settings, 'MATPLOTLIB_BACKEND', 'Agg')

FORMATS = getattr(settings, 'MATPLOTLIB_FORMATS', DEFAULT_FORMATS)
assert isinstance(FORMATS, dict)

# == MPLCONFIGDIR ==
# Writable directory for matplotlib configuration data
# If env. variable MPLCONFIGDIR is set it will be used
# Otherwise MPLCONFIGDIR from settings file will be used
# If none of the above provided will default to /tmp/.matplotlib
# IMPORTANT: MPLCONFIGDIR must be set prior to importing matplotlib
try:
    MPLCONFIGDIR = os.environ["MPLCONFIGDIR"]
except KeyError:
    MPLCONFIGDIR = getattr(settings, 'MPLCONFIGDIR', DEFAULT_MPLCONFIGDIR) 
    # os.putenv("MPLCONFIGDIR", MPLCONFIGDIR)
    os.environ["MPLCONFIGDIR"] = MPLCONFIGDIR
    
# TODO: check/set env var MATPLOTLIBRC
# == MATPLOTLIB_RC_PARAMS ==
# Allows to set site-wide matplotlib properties
RC_PARAMS = getattr(settings, 'MATPLOTLIB_RC_PARAMS', None)
if RC_PARAMS:
    import matplotlib
    for k,v in RC_PARAMS.items():
        matplotlib.rcParams[k] = v
    

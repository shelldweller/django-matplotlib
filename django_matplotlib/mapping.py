"""
Mappings to translate URL arguments into kwargs
"""

# FUNCTIONS FOR CONVERTING URL STRING REPRESENTATIONS INTO
# PYTHON OBJECTS SUITABLE FOR CREATING PLOTS

# identity function
noop = lambda x: x


def str2num(value):
    """
    Takes a string and returns its numeric representation.
    ValueError will be raised if the string does not represent
    a valid number. Strings with decimals will be converted to
    floats. Otherwise integer conversion will take place.
    """
    if "." in value:
        return float(value)
    return int(value)

def str2bool(value):
    """Returns a boolean. False values are represented by "0" and True by "1"."""
    return bool(str2num(value))

def str2numlist(value):
    """
    Converts a string consisting of coma separated digits into a list of numbers.
    """
    return map(str2num, value.split(","))

def str2strlist(value):
    """
    Converts comma separated strings into a list of strings.
    """
    return value.split(",")

class ValueSelection(object):
    """
    Allows only a single selection from the list of values passed to init method.
    The first argument will be used as default if attampting to validate an invalid
    argument. Example:
    
        callable = ValueSelection("one","two","three")
        callable("two") # "two"
        callable("foo") # "one" (the default output for invalid input)
    """
    def __init__(self, *args):
        self.choices = set(args)
        self.default = args[0]
    
    def __call__(self, value):
        if value in self.choices:
            return value
        return self.default

# MAPPING DEFINES KWARGS AND CONVERSION FUNCTIONS FOR EACH
# PLOT TYPE
MAPPING = {
    "pie" : {
        "x" : str2numlist,
        "explode" : str2numlist,
        "labels" : str2strlist,
        "colors" : str2strlist,
        "autopct" : noop,
        "pctdistance" : str2num,
        "labeldistance" : str2num,
        "shadow" : str2bool,
    },
    "bar" : {
        "left" : str2numlist,
        "height" : str2numlist,
        "width" : str2num,
        "bottom" : str2numlist,
        "color" : str2strlist,
        "edgecolor" : str2strlist,
        "xerr" : str2numlist,
        "yerr" : str2numlist,
        "ecolor" : noop,
        "capsize" : str2num,
        # error_kw not supported
        "align" : ValueSelection("edge","center"),
        #"orientation" : ValueSelection("vertical","horizontal") doesn't seem to work properly
        "log" : str2bool,
        "antialiased": str2bool,
        "fill" : str2bool,
        "hatch" : ValueSelection("/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"),
        "label" : noop,
        "ls" : ValueSelection("solid", "dashed", "dashdot", "dotted"),
        "lw" : str2num,
    }
}

KNOWN_CHART_LIST = MAPPING.keys()

MAPPING["figure"] = {
    # TODO: figsize is in inches; it would be nice to define size in pixels
    "figsize" : str2numlist,
    # commented values do not seem to work
    #"dpi" : str2num,
    #"facecolor" : noop,
    #"edgecolor" : noop,
    #frameon
}

# ADDITIONAL MAPPING FOR NON CHARTS

# MAPPING FUNCTION
def extract_kwargs(key, dic):
    """
    Extracts keyword arguments from dictionary for proper mapping.
    
    Arguments:
    - `key` is the name of plot function to be drawn (e.g., "pie")
    - `dic` is a dictionary like object of string literals to be converted
        to keyword arguments. Unknown entries will be ignored.
    
    Sample usage:
    
        # assuming `ax` is a subplot object
        # and `request` is an instance of Django's HTTPRequest
        ax.pie( **extract_kwargs("pie", request.GET) )
    """
    mapping = MAPPING[key]
    kwargs = {}
    for kwarg,func in mapping.items():
        if kwarg in dic:
            kwargs[kwarg] = func(dic.get(kwarg))
    return kwargs
#
#x, explode=None, labels=None,
#    colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'),
#    autopct=None, pctdistance=0.6, labeldistance=1.1, shadow=False
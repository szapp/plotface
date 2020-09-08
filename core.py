"""
Functions for switching between dark and light as well as inline and gui
"""

from matplotlib import pyplot as plt
from IPython import get_ipython


_light = 0
_dark = 1
_state_str = [
    'light',
    'dark'
]
_state = _light


def getstate(num=False):
    return _state if num else _state_str[_state]


def _setstate(new):
    global _state
    _state = new


def dark(afc='none', style='dark_background'):
    """
    Adjust figure interface to a dark background
    """
    rc_dark = dict(plt.style.core.library.get(style, {}))
    rc_dark.pop('savefig.facecolor', None)
    rc_dark.pop('savefig.edgecolor', None)
    rc_dark.update({
        'axes.facecolor': afc,
        'figure.facecolor': 'none',
        'figure.edgecolor': 'white',
        'legend.facecolor': (0.153, 0.157, 0.133, 0.789),
        'legend.edgecolor': 'white',
        'legend.framealpha': None,  # Causes issues with facecolor
    })
    plt.rcParams.update(rc_dark)
    _setstate(_dark)


def light(bg='white'):
    """
    Adjust figure interface to a light background (as is default)
    """
    rc_light = {
        'lines.color': 'black',
        'patch.edgecolor': 'black',
        'text.color': 'black',
        'axes.edgecolor': 'black',
        'axes.labelcolor': 'black',
        'axes.prop_cycle': plt.rcParamsDefault['axes.prop_cycle'],
        'xtick.color': 'black',
        'ytick.color': 'black',
        'grid.color': 'black',
        'figure.facecolor': bg,
        'figure.edgecolor': 'black',
        'boxplot.boxprops.color': 'black',
        'boxplot.capprops.color': 'black',
        'boxplot.flierprops.color': 'black',
        'boxplot.flierprops.markeredgecolor': 'black',
        'boxplot.whiskerprops.color': 'black',
        'legend.facecolor': 'inherit',
        'legend.edgecolor': 'black',
    }
    plt.rcParams.update(rc_light)
    _setstate(_light)


def inline(use_dark=False):
    """
    Set matplotlib to inline backend
    """
    get_ipython().run_line_magic('matplotlib', 'inline')
    get_ipython().run_line_magic('config', 'InlineBackend.close_figures=True')
    plt.ion()
    if use_dark:
        dark()
    else:
        light()


def gui(gui='qt'):
    """
    Set matplotlib to gui backend and reset to light interface
    """
    get_ipython().run_line_magic('matplotlib', gui)
    get_ipython().run_line_magic('config', 'InlineBackend.close_figures=False')
    plt.ioff()
    light()

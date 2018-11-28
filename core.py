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


def dark():
    """
    Adjust figure interface to a dark background
    """
    rc_dark = {
        "text.color": "white",
        "axes.labelcolor": "white",
        "axes.edgecolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "figure.facecolor": "none",
    }
    plt.rcParams.update(rc_dark)
    _setstate(_dark)


def light(bg='white'):
    """
    Adjust figure interface to a light background (as is default)
    """
    rc_light = {
        "text.color": "black",
        "axes.labelcolor": "black",
        "axes.edgecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "figure.facecolor": bg,
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

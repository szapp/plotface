"""
Plotface
========

Switch between a light or dark interface of matplotlib figures as well
as between inline and gui plotting for IPython on the fly.

To keep having figures saved with black lines and text, the package hooks the
savefig function on loading to allow replacing the color of all white text and
lines with black in case the dark interface is selected.
"""

from matplotlib import pyplot as plt
from .core import (
    getstate,
    dark,
    light,
    inline,
    gui,
)

__all__ = [
    'dark',
    'light',
    'getstate',
    'inline',
    'gui',
    'unload',
]


try:
    _savefig_orig
except NameError:
    _savefig_orig = plt.Figure.savefig


def _apply(obj, oldcolor, newcolor):
    if hasattr(obj, 'get_color') and obj.get_color() in oldcolor:
        obj.set_color(newcolor)
        return True
    elif hasattr(obj, 'get_edgecolor') and obj.get_edgecolor() in oldcolor:
        obj.set_edgecolor(newcolor)
        return True
    elif isinstance(obj, list):
        for i in obj:
            _apply(i, oldcolor, newcolor)
        return True
    return False


def _savefig_new(self, fname, **kwargs):
    if getstate() == 'dark':
        obj = []
        for ax in self.get_axes():
            for c in (ax.get_children()
                      + ax.xaxis.get_children()
                      + ax.yaxis.get_children()
                      + ax.xaxis.get_ticklines()
                      + ax.yaxis.get_ticklines()
                      + ax.xaxis.get_ticklabels()
                      + ax.yaxis.get_ticklabels()):
                if _apply(c, ['white', (1, 1, 1, 1)], 'black'):
                    obj.append(c)

    _savefig_orig(self, fname, **kwargs)
    if getstate() == 'dark':
        for o in obj:
            _apply(o, ['black', (0, 0, 0, 1)], 'white')


plt.Figure.savefig = _savefig_new


def unload():
    """
    Unload the savefig hook and revert to the light interface
    """
    plt.Figure.savefig = _savefig_orig
    light()

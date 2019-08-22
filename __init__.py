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
    changed = False

    # Fill color
    if hasattr(obj, 'get_color'):
        colr = obj.get_color()  # Special case if it is a numpy array
        if not isinstance(colr, (tuple, str)):
            colr = tuple(colr)
        if colr in oldcolor:
            obj.set_color(newcolor)
            changed = True

    # Face color (or multiple face colors for collections)
    if hasattr(obj, 'get_facecolor'):
        if not isinstance(obj.get_facecolor(), (tuple, str)):
            colors_b4 = [tuple(i) if not isinstance(i, (tuple, str)) else i
                         for i in obj.get_facecolor()]
            colors = [tuple(i) if not isinstance(i, (tuple, str)) else i
                      for i in obj.get_facecolor()]
            colors = [newcolor if i in oldcolor else i for i in colors]
            if colors != colors_b4:
                changed = True
                obj.set_facecolor(colors)
        elif obj.get_facecolor() in oldcolor:
            obj.set_facecolor(newcolor)
            changed = True

    # Edge color (or multiple edge colors for collections)
    if hasattr(obj, 'get_edgecolor'):
        if not isinstance(obj.get_edgecolor(), (tuple, str)):
            colors_b4 = [tuple(i) if not isinstance(i, (tuple, str)) else i
                         for i in obj.get_edgecolor()]
            colors = [tuple(i) if not isinstance(i, (tuple, str)) else i
                      for i in obj.get_edgecolor()]
            colors = [newcolor if i in oldcolor else i for i in colors]
            if colors != colors_b4:
                changed = True
                obj.set_edgecolor(colors)
        elif obj.get_edgecolor() in oldcolor:
            obj.set_edgecolor(newcolor)
            changed = True

    # Marker colors
    if hasattr(obj, 'get_markerfacecolor'):
        colr = obj.get_markerfacecolor()  # Special case if it is a numpy array
        if not isinstance(colr, (tuple, str)):
            colr = tuple(colr)
        if colr in oldcolor:
            obj.set_markerfacecolor(newcolor)
            changed = True
    if hasattr(obj, 'get_markeredgecolor'):
        colr = obj.get_markeredgecolor()  # Special case if it is a numpy array
        if not isinstance(colr, (tuple, str)):
            colr = tuple(colr)
        if colr in oldcolor:
            obj.set_markeredgecolor(newcolor)
            changed = True

    return changed


def _savefig_new(self, fname, **kwargs):
    if getstate() == 'dark':
        # Collect all objects from the figure
        pool = self.get_children()

        # Recurse into children
        for ele in pool:
            if hasattr(ele, 'get_children'):
                pool += ele.get_children()
            elif isinstance(ele, list):
                pool.remove(ele)
                pool += ele

        # Iterate over all objects
        obj = []
        for c in set(pool):
            if _apply(c, ['w', 'white',
                          (1, 1, 1, 1),
                          (0.8, 0.8, 0.8, 0.8)],  # Legend
                      'black'):
                obj.append(c)

        # Call original save function
        _savefig_orig(self, fname, **kwargs)

        # Restore original colors
        for o in obj:
            if not _apply(o, ['black', (0, 0, 0, 1)], 'white'):
                _apply(o, [(0, 0, 0, 0.8)], (0.8, 0.8, 0.8, 0.8))  # Legend
    else:
        # Light interface: No changes
        _savefig_orig(self, fname, **kwargs)


def _load():
    """
    Apply the savefig hook
    """
    plt.Figure.savefig = _savefig_new


def unload():
    """
    Unload the savefig hook and revert to the light interface
    """
    plt.Figure.savefig = _savefig_orig
    light()


# Apply hook on initialization
_load()

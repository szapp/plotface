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


def _isnested(coll):
    if hasattr(coll, '__len__'):
        if len(coll) > 4:
            return True
        for c in coll:
            if not isinstance(c, (tuple, str)) and hasattr(c, '__len__'):
                return True
    return False


def _apply(obj, oldcolor, newcolor):
    attributes = [
        'color',
        'facecolor',
        'edgecolor',
        'markerfacecolor',
        'markeredgecolor',
    ]

    changed = False
    for attr in attributes:
        getter = 'get_' + attr
        setter = 'set_' + attr

        if not hasattr(obj, getter) or not hasattr(obj, setter):
            continue

        getter = getattr(obj, getter)
        setter = getattr(obj, setter)

        # Skip empty collections
        if hasattr(getter(), '__len__') and len(getter()) == 0:
            continue

        # Change shallow, non-tuple collections into tuples
        if not isinstance(getter(), str) and not _isnested(getter()):
            setter(tuple(getter()))

        # Recurse into collections
        if not isinstance(getter(), (tuple, str)):
            colors_b4 = [tuple(i) if not isinstance(i, (tuple, str)) else i
                         for i in getter()]
            colors = [newcolor if i in oldcolor else i for i in colors_b4]
            if colors != colors_b4:
                setter(colors)
                changed = True
        elif getter() in oldcolor:
            setter(newcolor)
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

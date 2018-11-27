# plotface

Python module to switch between light/dark interface and inline/gui backend of matplotlib figures in IPython on the fly.


## Installation

Clone `plotface` into a directory in your python path.

```bash
git clone https://github.com/szapp/plotface.git
cd plotface
pip install -r requirements.txt
```


## Usage

```python
In [1]: import plotface

In [2]: plotface.dark()

In [3]: plotface.light()

In [4]: plotface.inline()

In [5]: plotface.gui()
```

To keep having figures saved with black lines and text regardless of light or dark interface, the module hooks the
`savefig` function of matplotlib's pyplot to replace the color of all white text and lines with black.

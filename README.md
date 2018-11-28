# plotface

Python module to switch between light/dark interface and inline/gui backend of matplotlib figures in IPython on the fly.

It is particularly useful when running a Jupyter or IPython console embedded in a dark themed shell, as for example
when using [Spyder](https://www.spyder-ide.org) with color schemes like Monokai or similar ([see below](#example)).


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


## Example

This example shows the aesthetic benefit of switching to a dark interface when working with the Monokai color scheme.

![](https://user-images.githubusercontent.com/20203034/49161136-87f4aa00-f328-11e8-9c79-97cb89e2688a.png)


## Saving Figures

To keep having figures saved with black lines and text regardless of light or dark interface, the module hooks the
`savefig` function of matplotlib's pyplot to replace the color of all white text and lines with black.

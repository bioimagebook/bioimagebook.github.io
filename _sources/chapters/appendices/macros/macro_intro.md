---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.7.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(chap_macro_intro)=
# ImageJ: Writing macros 

:::{admonition} Chapter outline 
:class: tip

* Processing & analysis steps in ImageJ can be automated by writing **macros**
* Straightforward macros can be produced without any programming using the **Macro Recorder**
* Recorded macros can be modified to make them more robust & suitable for a wider range of images 
::: 

```{code-cell} ipython3
:tags: [hide-cell, thebe-init]

%load_ext autoreload
%autoreload 2

# Default imports
import sys
sys.path.append('../../../')
from helpers import *
from matplotlib import pyplot as plt
from myst_nb import glue
import numpy as np
from scipy import ndimage
```

## Introduction 

It's one thing to figure out steps that enable you to analyze an image, it's quite another to implement these steps for several -- and perhaps many -- different images.
Without automation, the analysis might never happen;
all the mouse-moving and clicking would just be too time-consuming, error-prone or boring, and momentarily lapses in concentration could require starting over again. 

Even a brief effort to understand how to automate analysis can produce vast, long-lasting improvements in personal productivity and sanity by reducing the time spent on mind-numbingly repetitive tasks.
In some straightforward cases (e.g.
converting file formats, applying projections or filters, or making measurements across entire images), this can already be done in ImageJ using the commands in the {menuselection}`Process --> Batch -->` submenu and no programming whatsoever.
But it's also very worthwhile to get some experience in producing macros, scripts or plugins, after which you can add your own new commands to the menus and carry out customized algorithms with a single click of a button or press of a key. 

### What's a macro?

Macros are basically sequences of commands, written in some programming language (here ImageJ's own macro language), which can be run automatically to make processing faster and easier.

The following sections are far from an extensive introduction to macro-writing, but rather aim to introduce the main ideas quickly using two worked examples.
Should you wish to delve deeper into the subject, there's an [introduction to the language on the ImageJ website](https://imagej.net/developer/macro/macros.html) [^fn_1], and a [very helpful tutorial on the ImageJ wiki](https://imagej.net/Introduction_into_Macro_Programming) [^fn_2], while the list of [built-in macro functions](https://imagej.net/developer/macro/functions.html) is an indispensable reference [^fn_3].

:::{admonition} Use Fiji's 'Script editor'
:class: tip

Although it's possible to use ImageJ rather than Fiji to create macros, Fiji's script editor makes the process *much* easier by coloring text according to what it does.
I will assume that you are using this. 
:::

:::{admonition} From macros to scripts
Once confident with macros, the next step would be to enter the world of scripts and plugins.
These can be somewhat more difficult to learn, but reward the effort with the ability to do more complicated things.
Links to help with this are available at https://imagej.net/Scripting. 
:::


[^fn_1]: <https://imagej.net/developer/macro/macros.html>

[^fn_2]: <https://imagej.net/Introduction_into_Macro_Programming>

[^fn_3]: <https://imagej.net/developer/macro/functions.html>

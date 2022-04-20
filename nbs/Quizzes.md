---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [hide-cell, thebe-init]

%load_ext autoreload
%autoreload 2

# Default imports
import sys
sys.path.append('../')
from helpers import *
from matplotlib import pyplot as plt
from myst_nb import glue
import numpy as np
from scipy import ndimage
```

```{code-cell} ipython3
im1 = load_image('disguise1.png').astype(np.float32)
im2 = load_image('disguise2.png').astype(np.float32)
im3 = im1.copy()
im4 = im2.copy()

# Transfer mean & standard deviation
im2 -= im2.mean()
im2 /= im2.std()
im2 *= im1.std()
im2 += im1.mean()

from imageio import imwrite
import os
os.makedirs('data', exist_ok=True)

images = (im1, im2, im3, im4)
for ii, im in enumerate(images):
    name = f'disguise{ii+1}.tif'
    print((name, im.min(), im.max(), im.mean(), im.std()))
    show_image(im, pos=(1, len(images), ii+1), title=name)
    imwrite(f'data/{name}', im)
```

```{code-cell} ipython3
im1 = load_image('disguise1.png').astype(np.float32)
im2 = load_image('disguise2.png').astype(np.float32)

# Transfer mean & standard deviation
im2 -= im2.mean()
im2 /= im2.std()
im2 *= im1.std()
im2 += im1.mean()

# Create an image that doesn't quite match
im3 = im1.copy()
noise = np.random.default_rng().random(im3.shape) * 2
bw = np.abs(im3 - im3.mean()) < im3.std()
im3[bw] += noise[bw]
im3[im3 > im1.max()] = im1.max()
im3[im3 < im1.min()] = im1.min()

# Create duplicate
im4 = im1.copy()

from imageio import imwrite
import os
os.makedirs('data', exist_ok=True)

imwrite(f'data/disguise_matching.tif', im1)
imwrite(f'data/disguised_1.tif', im3)
imwrite(f'data/disguised_2.tif', im2)
imwrite(f'data/disguised_3.tif', im4)


images = (im1, im2, im3, im4)
for ii, im in enumerate(images):
    name = f'disguised_{ii}.tif'
    print((name, im.min(), im.max(), im.mean(), im.std()))
    show_image(im, pos=(1, len(images), ii+1), title=name)
    imwrite(f'data/{name}', im)
```

```{code-cell} ipython3

```

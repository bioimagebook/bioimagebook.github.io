---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

# Python:  Pixel size & dimensions

This section gives a bit of background on working with pixel sizes and dimensions in Python... which is a bit more complicated than one might first expect.

```{code-cell} ipython3
# First, our usual default imports
import sys
sys.path.append('../../../')

from helpers import *
import matplotlib.pyplot as plt
import numpy as np
```

## Pixel size

Checking the pixel size in Python has been, in my opinion, a bit of a pain - because the common libraries used to read images don't always make that information very easy to access.

The situation is improving though.

Here, we'll look at accessing pixel size information using two popular image-reading libraries:
* [`imageio`](https://pypi.org/project/imageio/) - which very commonly used, and makes reading lots of common image types straightforward
* [`bioio`](https://bioio-devs.github.io/bioio) - which is a bit more complex, but has some *extremely* useful features for working with scientific images

+++

### ImageIO

To explore pixel sizes with `imageio`, let's return to the neuron image used in the 'Channels & colors' chapter.

The following code shows how we can read both the pixel values and the metadata.

```{code-cell} ipython3
# In preparation for the future, we'll use the 'v3' imageio process
import imageio.v3 as iio

# Get the path to the image (this is a specific helper function for this book)
path = find_image('Rat_Hippocampal_Neuron.tif')[0]

# Read the pixel values
im_iio = iio.imread(path)

# Read & print the metadata
metadata = iio.immeta(path)
print(metadata)
```

The metadata contains a lot of info, even including lookup tables.

Printing it a little more nicely (and skipping the LUTs), we get:

```{code-cell} ipython3
for k, v in metadata.items():
    if not 'LUTs' in k:
        print(f'{k}: {v}')
```

This metadata is actually quite ImageJ-specific, and other TIFFs may give quite different metadata.

We can see the version of ImageJ that wrote the file, but picking out the key thing we want here - the pixel size - is not so easy.

Seeing `unit=um` is encouraging, but not enough.

We can explore a bit more with 'properties', which imageio described as ['a curated set of standardized metadata'](https://imageio.readthedocs.io/en/v2.30.0/reference/userapi.html#metadata).

```{code-cell} ipython3
properties = iio.improps(path, extension=".tif")
print(properties)
```

Here, the `spacing=(6.25, 6.25)` seems promising.

It's tempting to suppose that means the pixel width and height are both 6.25 µm - *however* if I check the same image in ImageJ itself, I see the pixel width and height are actually 0.16 µm... which happens to equal 1.0/6.25 µm.

```{code-cell} ipython3
print(1.0 / 6.25)
```

Therefore the information **is** in the metadata, but it's very easy to misinterpret - and it isn't even guaranteed to be correct if the image was written by some other software.

So while `imageio` is excellent for reading images easily - generally just a quick `im = imread(path)` - it's not necessarily the best thing to use when pixel sizes (or other metadata) matter.

+++

### Using BioIO

The best alternative I know for working with scientific (especially biomedical) images is [**BioIO**](https://bioio-devs.github.io/bioio) (the successor to [AICSImageIO](https://github.com/AllenCellModeling/aicsimageio)).
This is a really useful Python library that standardizes reading and writing multiple file formats - and, depending upon how it's installed, can even access lots more awkward proprietary file formats with the help of [Bio-Formats](http://www.openmicroscopy.org/bio-formats/).

Although it's possible to use a version of `imread` with BioIO, it's worth learning the alternative way of doing things by creating an `BioImage` object.
This provides us with a way to access pixels and lots of other useful things whenever we need them.

```{code-cell} ipython3
from bioio import BioImage

# Create a BioImage
img_bio = BioImage(path)

# Print its main attributes
print(img_bio)
for d in dir(img_bio):
    if not d.startswith('_'):
        print(d)
```

From this, we can immediately see the attribute that will provide us with pixel sizes directly.

```{code-cell} ipython3
print(img_bio.physical_pixel_sizes)
```

One perhaps non-obvious thing to know when using BioIO is that the `BioImage` isn't a regular NumPy array of the kind that `imageio.imread` would return.
Rather, if you want that, you need to request the data.

Using this knowledge, we can check that we have the same mean pixel value for both - as a quick way to ascertain that the actual pixel values are likely to match.

```{code-cell} ipython3
print(f'Mean pixel value from imageio:      {im_iio.mean():.2f} (total pixel count {im_iio.size})')
print(f'Mean pixel value from BioIO:        {img_bio.data.mean():.2f} (total pixel count {img_bio.data.size})')
```

## Dimensions

### Array shapes and dimensions

We've seen how two different libraries can enable us to read the same pixel values as NumPy arrays and extract pixel size information.

We might well expect that the NumPy arrays representing the pixel values are the same, but in fact we can't count on that.

NumPy is incredibly flexible when it comes to handling multidimensional arrays. 
And while that flexibility can be really helpful, it can also complicate things.

To see it in action, let's check the dimensions of the images we read using imageio and BioIO.

```{code-cell} ipython3
# Print shape of image read by imageio
import imageio.v3 as iio
path = find_image('Rat_Hippocampal_Neuron.tif')[0]
im_iio = iio.imread(path)
print(f'Shape of image read by imageio:     {im_iio.shape}')

# Print shape of image read by bioio
from bioio import BioImage
im_bio = BioImage(path).data
print(f'Shape of image read by BioIO: {im_bio.shape}')

print(f'Arrays the same? {np.array_equal(im_bio, im_iio)}')
```

We can see the number of pixels are the same, but there are some extra 'singleton' dimensions stuck into the results from BioIO (i.e. with length `1`).

Fortunately, we can easily remove them with an `np.squeeze` - and end up with the same arrays.

```{code-cell} ipython3
im_bio_squeezed = np.squeeze(im_bio)
print(f'Shape of image read by BioIO & squeezed: {im_bio_squeezed.shape}')

print(f'Arrays the same? {np.array_equal(im_bio_squeezed, im_iio)}')
```

So a natural question is: **why has BioIO snuck in some extra dimensions?**

Before answering that, we should ask ourselves something else.
**What exactly do we _have_ along the dimension of length `5`?**

And this is where things aren't terribly clear with imageio.

`5` *could* be the width of the image, height of the image, number of channels, number of z-slices, or number of timepoints.

Based upon our knowledge of images and the other dimensions, we'd be justified in expecting that the `5` doesn't correspond to the image width or height - `512` seems more likely for those - so it's probably one of the others.

But the problem is that **we have no way of knowing** without further information.
If we don't have some external source to tell us, we need to poke around the metadata or look at the contents to figure out the answer.

```{code-cell} ipython3
# Loop through the first dimension and show images for each plane
n_slices = im_iio.shape[0]
plt.figure(figsize=(12, 4))
for ii in range(n_slices):
    plt.subplot(1, n_slices, ii+1)
    plt.title(f'Plane {ii+1}')
    show_image(im_iio[ii], clip_percentile=1)
```

To me, that looks very much like we have 5 different channels.
I'm making some assumptions there... but they seem pretty safe assumptions.

However BioIO removes this ambiguity in a couple of ways.
1. You can expect `BioIO` to return a 5D array, with the dimensions in a consistent order: `TCZYX` (although there is at least one caveat in the next section!)
2. You can easily query the dimensions and order to be sure

```{code-cell} ipython3
image = BioImage(path)
print(image.dims)
print(f'Shape: {image.dims.shape}')
print(f'Order: {image.dims.order}')
```

### Where are my channels?!?

We've seen above that imageio can return a 5-channel image with the channels first.
Our question here is: does it always do that?

The answer, alas, is no.
The location of the channels dimensions is painfully uncertain in Python, and often different tools expect it to be in different places.

Or sometimes the *same* tool might put it in a different place.

To see that in action, let's read a simple RGB image with imageio.

```{code-cell} ipython3
path = find_image('leaf.jpg')[0]
im_iio = iio.imread(path)
print(im_iio.shape)
```

An RGB image has 3 channels - red, green and blue - but it seems that suddenly we have the channels dimension last.

Why?

I don't have a very satisfying explanation, except to say that for RGB that's often what you want because matplotlib expects the channels to be last, and we often use matplotlib to show images.

```{code-cell} ipython3
# Show an RGB image with channels-last using matplotlib
from matplotlib import pyplot as plt

path = find_image('leaf.jpg')[0]
im_iio = iio.imread(path)
plt.imshow(im_iio)
plt.show()
```

It's not *always* what you want though, and if you get enough deep learning then you'll find the 'channels-first' or 'channels-last' question coming up often.

With that in mind, we can use NumPy to shift from so-called 'channels-last' to 'channels-first' - but matplotlib won't like that very much.

```{code-cell} ipython3
# *Try* to show an RGB image with channels-first using matplotlib

im_iio_channels_first = np.moveaxis(im_iio, source=-1, destination=0)
print(f'My new shape: {im_iio_channels_first.shape}')

try:
    plt.imshow(im_iio_channels_first)
    plt.show()
except Exception as ex:
    print(f"I can't show that, sorry! {ex}")
```

So imageio might get channels at the start or the end.
For RGB, it seems to prefer the end.

What does BioIO do?

Since I said BioIO is consistent, I'd like to say it puts the channels in the same place for the RGB and 5-channel image... but no.
It also treats RGB as a special case.

```{code-cell} ipython3
image = BioImage(path)

print(image.shape)
print(image.dims.order)
```

It's a little hard to find, but the BioIO documentation mentions that [you can expect 5 dimensions for non-RGB images, but RGB images have 6 dimensions](https://bioio-devs.github.io/bioio/bioio.html#bioio.bio_image.BioImage.get_image_data) - where the sixth is called `S` for `Samples`.

The good thing is that, assuming you don't have anything else going on with the first 3 dimensions - i.e. they are just `(1, 1, 1)` - a simple `np.squeeze` is enough to convert the pixel array into a matplotlib-friendly channels-last RGB format.

+++

## More dimensions

We'll end this section by looking at an image with 2 channels and 25 z-slices.

> Since you now know how to explore the dimensions in detail, I'll use my `load_image` helper function for convenience... which returns a NumPy array that's pre-squeezed to remove any singleton dimensions.

```{code-cell} ipython3
im = load_image('confocal-series.zip')
print(f'Shape: {im.shape}')
```

Since we already considered how to view multichannel images in the last chapter, let's extract a single channel here.

```{code-cell} ipython3
# Channels come second
# This gives us all the z-slices (:), the first channel (0), everything else (...)
im_single = im[:, 0, ...]
print(f'New shape: {im_single.shape}')
```

At this point, NumPy becomes quite fun - because it is *so easy* to do stuff along different dimensions.

For example, we can rapidly generate different z-projections.

```{code-cell} ipython3
plt.figure(figsize=(16, 4))

plt.subplot(1, 4, 1)
plt.imshow(im_single.max(axis=0))
plt.axis(False)
plt.title('Max z-projection')

plt.subplot(1, 4, 2)
plt.imshow(im_single.min(axis=0))
plt.axis(False)
plt.title('Min z-projection')

plt.subplot(1, 4, 3)
plt.imshow(im_single.mean(axis=0))
plt.axis(False)
plt.title('Mean z-projection')

plt.subplot(1, 4, 4)
plt.imshow(im_single.std(axis=0))
plt.axis(False)
plt.title('Std.dev. z-projection')

plt.show()
```

But we're not limited to projecting along z - we can just switch the `axis` value and project along some other dimension.

> Note that this won't do any correction for differences in pixel size in xy vs. z. With only 25 z-slices, these projections look extremely squashed.

```{code-cell} ipython3
plt.figure(figsize=(16, 4))

plt.subplot(1, 4, 1)
plt.imshow(im_single.max(axis=1))
plt.axis(False)
plt.title('Max y-projection')

plt.subplot(1, 4, 2)
plt.imshow(im_single.min(axis=1))
plt.axis(False)
plt.title('Min y-projection')

plt.subplot(1, 4, 3)
plt.imshow(im_single.mean(axis=1))
plt.axis(False)
plt.title('Mean y-projection')

plt.subplot(1, 4, 4)
plt.imshow(im_single.std(axis=1))
plt.axis(False)
plt.title('Std.dev. y-projection')

plt.show()
```

And we can also slice wherever we like as well, to obtain orthogonal views.

```{code-cell} ipython3
plt.figure(figsize=(8, 8))

plt.subplot(2, 2, 1)
plt.imshow(im_single[im_single.shape[0]//2, ...])
plt.axis(False)
plt.title('Middle z-slice')

plt.subplot(2, 2, 3)

plt.imshow(im_single[:, im_single.shape[1]//2, ...])
plt.axis(False)
plt.title('Middle row')

plt.subplot(2, 2, 2)
plt.imshow(im_single[..., im_single.shape[2]//2].transpose())
plt.axis(False)
plt.title('Middle column')

plt.tight_layout()
plt.show()
```

```{code-cell} ipython3

```

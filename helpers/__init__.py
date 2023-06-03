from pathlib import Path
from zipfile import ZipFile
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
from pathlib import Path
from myst_nb import glue
from typing import Dict, List, Tuple, Union, IO, Iterable, Sequence

DEFAULT_DPI = 200

# Default colors (from names)
_default_colors = dict(
        red=(1,0,0),
        green=(0,1,0),
        blue=(0,0,1),
        magenta=(1,0,1),
        yellow=(1,1,0),
        cyan=(0,1,1),
        white=(1,1,1),
        black=(0,0,0)
    )

def glue_images(glue_label: str, images: Union[str, List], figsize=None, dpi=300, plot_shape=None, **kwargs):
    if isinstance(images, str):
        images = images[images]
        
    n_rows = 1 if not plot_shape else plot_shape[0]
    n_cols = len(images) if not plot_shape else plot_shape[1]
    if not figsize:
        default_width = 12
        figsize = (default_width, default_width/n_cols*n_rows)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    
    for ii, image in enumerate(images):
        plt.subplot(n_rows, n_cols, ii+1)
        title = None
        if isinstance(image, str):
            im = load_image(image)
        else:
            im = load_image(image[0])
            if len(image) > 2:
                title = image[1]    
        plt.imshow(im, **kwargs)
        if title:
            plt.title(title)
        plt.axis(False)
    glue(glue_label, fig, display=False)
    plt.close()


def create_figure(figsize=None, dpi=DEFAULT_DPI, **kwargs):
    return plt.figure(figsize=figsize, dpi=dpi, **kwargs)

def show_image(im, pos=None, axis=False, title=None, axes=None, cmap='gray', clip_percentile=None,
        fontdict={'fontsize':'small'}, **kwargs):
    """
    Helper function to show an image using pyplot.
    """
    if pos:
        if isinstance(pos, int):
            plt.subplot(pos)
        else:
            plt.subplot(*pos)
    if type(im) in [str, bytes, Path]:
        im = _load_image(im)
    if clip_percentile:
        kwargs = dict(kwargs)
        if not 'vmin' in kwargs:
            kwargs['vmin'] = np.percentile(im, clip_percentile)
        if not 'vmax' in kwargs:
            kwargs['vmax'] = np.percentile(im, 100-clip_percentile)
    if axes is not None:
        axes.imshow(im, cmap=cmap, **kwargs)
        if title:
            axes.set_title(title, fontdict=fontdict)
        if axis:
            axes.set_axis_on()
        elif axis is not None:
            axes.set_axis_off()
    else:
        plt.imshow(im, cmap=cmap, **kwargs)
        if title:
            plt.title(title, fontdict=fontdict)
        plt.axis(axis)
            
def add_colorbar(**kwargs):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    if 'orientation' in kwargs and kwargs['orientation'] == 'horizontal':
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("bottom", size="5%", pad=0.05)
        plt.colorbar(**kwargs, cax=cax)
    else:
        plt.colorbar(**kwargs)


def show_plot(*args, pos=None, axis=True, axes=None, bins=None,
                   xlabel=None, ylabel=None, 
                   xlim=None, ylim=None,
                   title=None, color=(0.1, 0.1, 0.2, 0.6), linewidth=1, fontdict={'fontsize':'small'}, **kwargs):
    if pos:
        if isinstance(pos, int):
            ax = plt.subplot(pos)
        else:
            ax = plt.subplot(*pos)
    elif axes is not None:
        ax = axes
    else:
        ax = plt.gca()
        
    ax.plot(*args, color=color, linewidth=linewidth, **kwargs)
    if title:
        ax.set_title(title, fontdict=fontdict)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if ylim:
        ax.set_ylim(ylim)
    if xlim:
        ax.set_xlim(xlim)
    if axis:
        ax.set_axis_on()
    elif axis is not None:
        ax.set_axis_off()
    
def show_histogram(im, pos=None, axis=True, axes=None, bins=None, xlabel='Pixel value', ylabel='Count', 
                   title=None, color=(0.1, 0.1, 0.2, 0.6), fontdict={'fontsize':'small'},
                   stats=None, **kwargs):
    """
    Helper function to show an image histogram using pyplot.
    """
    if pos:
        if isinstance(pos, int):
            ax = plt.subplot(pos)
        else:
            ax = plt.subplot(*pos)
    elif axes is not None:
        ax = axes
    else:
        ax = plt.gca()
    if type(im) in [str, bytes, Path]:
        im = load_image(im)
    if bins is None:
        bins = int(np.ceil(im.max()) - np.floor(im.min())) + 1
    
    data = im.flatten()
    n, bins, patches = ax.hist(data, bins=bins, color=color, **kwargs)
    
    if stats is not None:
        text = '\n'.join(
           [f'Mean: {data.mean():.1f}',
            f'Std.dev: {data.std():.1f}',
            f'Min: {data.min():.1f}',
            f'Max: {data.max():.1f}']
            )
        if stats == 'right' or (stats == 'auto' and np.argmax(n) <= len(n)/2):
            ax.text(0.95, 0.95, text, transform=ax.transAxes,
                horizontalalignment='right', verticalalignment='top', color=color, fontdict=fontdict)
        else:
            ax.text(0.05, 0.95, text, transform=ax.transAxes,
                horizontalalignment='left', verticalalignment='top', color=color, fontdict=fontdict)

    if title:
        ax.set_title(title, fontdict=fontdict)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if axis:
        ax.set_axis_on()
    elif axis is not None:
        ax.set_axis_off()

def glue_fig(glue_label: str, fig=None):
    if not fig:
        fig = plt.gcf
    glue(glue_label, fig, display=False)


def find_image(name: os.PathLike) -> Iterable[os.PathLike]:
    """
    Load a built-in image using imageio.
    
    Parameters
    ----------
    name: str, os.PathLike
      Name of the image, or full path to the image

    Returns
    -------
    an iterable of paths that match the requested image name 
    (usually of length 1, but may be empty or have more paths if there are duplicates)
    """
    # Check for full path
    if os.path.exists(name):
        return [Path(name)]
        
    path_current = Path()
    path_images = Path(__file__).parent.parent.joinpath('images')
    patterns = [
        (path_current, '**/' + name),
        (path_images, '**/' + name),
        (path_current, '**/' + name + '.*'),
        (path_images, '**/' + name + '.*')
    ]
    paths = []
    for path_base, pattern in patterns:
        for potential_path in path_base.glob(pattern):
            paths.append(potential_path)
    return paths


def load_image(name: Union[str, os.PathLike], volume: bool=False, metadata: bool=False, **kwargs) -> np.ndarray:
    """
    Load a built-in image using imageio.
    
    Parameters
    ----------
    name: str
      Name of the image, or full path to the image
    volume: bool
      Request that the image is read as a volume (using imageio.volread instead of imageio.imread)
    metadata:
      Request that the image metadata is returned as a second output

    Returns
    -------
    a numpy ndarray of pixel data, and optionally a second object containing metadata
    """
    for potential_path in find_image(name):
        try:
            if potential_path.suffix == '.zip':
                with ZipFile(potential_path, 'r') as zf:
                    names = zf.namelist()
                    if len(names) > 1:
                        print(f'Found {len(names)} entries in zip file - I will only try to read the first')
                    with zf.open(names[0]) as entry:
                        return _load_image(entry.read(), extension='.tif', volume=volume, metadata=metadata, **kwargs)
            else:
                return _load_image(potential_path, volume=volume, metadata=metadata, **kwargs)
        except Exception as err:
            print(err)
            print('Error reading image ', sys.exc_info()[0])
    raise FileNotFoundError(name)


def to_rgb(im: np.ndarray, color, vmin=None, vmax=None):
    """
    Apply a colormap to a single-channel image, converting it to an 8-bit RGB representation.
    """
    if color in _default_colors:
        color = _default_colors[color]
    if vmin is None:
        vmin = im.min()
    if vmax is None:
        vmax = im.max()
    im = im.astype(np.float32)
    im = np.clip(im, vmin, vmax)
    im = (im - vmin) * (255 / (vmax - vmin))
    im = np.atleast_3d(im) * np.array(color).reshape((1, 1, 3))
    return im.astype(np.uint8)

def merge_rgb(images: Iterable[np.ndarray]):
    """
    Merge multiple RGB images to create a composite image.
    Merging involves adding RGB values, clipping to the maximum permitted value
    (255 if the type is uint8, 1 otherwise).
    """
    im = None
    dtype = None
    for temp in images:
        if im is None:
            dtype = temp.dtype
            im = temp.copy().astype(np.float32)
        else:
            im += temp
    if dtype == np.uint8:
        im = np.clip(im, 0, 255)
    else:
        im = np.clip(im, 0, 1)
    return im.astype(dtype)



def create_rgb(im: np.ndarray, 
        colors: Sequence[Iterable[Union[float,str]]], 
        vmin: Iterable[float]=None, vmax: Iterable[float]=None,
        axis: int=None):
    """
    Create an RGB image from individual channels and associated single-color LUTs.
    
    Channels can be a list of tuples, each containing a 2D image channel and 
    a color (represented as a tuple of 3 floats).
    Alternatively, channels can be an ndarray with the colors provided as a separate 
    iterable.
    
    Image channels can be uint8 (in which case the output is uint8) or float.
    """
    im_merged = 0.0
    is_int = False

    if axis is None:
        if len(colors) == im.shape[0]:
            axis = 0
        elif len(colors) == im.shape[-1]:
            axis = len(im.shape) - 1
        else:
            raise ValueError(f'Unable to match {len(colors)} channels for image with shape {im.shape}')

    if np.issubdtype(im.dtype, np.integer):
        is_int = True
        im = im.astype(np.float32)

    channels = np.split(im, im.shape[axis], axis=axis)
    rescale_int = is_int
    vmin = vmin if isinstance(vmin, Sequence) else [vmin] * len(colors)
    vmax = vmax if isinstance(vmax, Sequence) else [vmax] * len(colors)
    
    for im_channel, color, vmi, vma in zip(channels, colors, vmin, vmax):
        if isinstance(color, str):
            color_tuple = _default_colors.get(color.lower())
        else:
            color_tuple = _default_colors.get(color, color)
        if vmi and vma:
            im_channel = (im_channel - vmi) / (vma - vmi)
        elif vmi:
            im_channel = (im_channel - vmi)
        elif vma:
            im_channel = im_channel / vma
        else:
            rescale_int = False
        im_merged += np.atleast_3d(im_channel) * np.asarray(color_tuple).reshape((1, 1, 3))
    
    if is_int:
        if rescale_int:
            im_merged = im_merged * 255
        return np.clip(im_merged, 0, 255).astype(np.uint8)
    else:
        return np.clip(im_merged, 0, 1.0)


def _load_image(data, volume:bool = False, metadata:bool = False, **kwargs):

    if metadata:
        return _load_image(data, metadata=False, **kwargs), iio.immeta(data, **kwargs)
    else:
        im = iio.imread(data, **kwargs)
        if volume:
            return im
        else:
            # If we don't want a volume image, try to squeeze down to the minimum
            # This is partly due to blobs.gif having a shape (1, ?, ?, 3) when it should really be single-channel grayscale
            im = np.squeeze(im)
            if im.ndim == 3 and im.shape[2] == 3 and np.array_equal(im[..., 0], im[..., 1]) and np.array_equal(im[..., 0], im[..., 2]):
                return im[..., 0]
            return im
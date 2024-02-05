Changelog
=========

This page summarizes the main changes.
To see all changes, check out the [commit log](https://github.com/bioimagebook/bioimagebook.github.io/commits/main).

## 5 February 2024
* Add initial support for translations
  * With huge thanks to @bethac07!

## 4 February 2024
* Dependency updates
  * matplotlib, numpy, bandas, scikit-image, scipy

## 18 November 2023
* Add copyright note to each page (thanks to @haesleinhuepf)
  * https://github.com/bioimagebook/bioimagebook.github.io/issues/28
* Rename & update 'License & Reuse' section for clarity
* Fix typo (thanks to @PeteHaitch)
  * https://github.com/bioimagebook/bioimagebook.github.io/pull/27

## 3 June 2023

* Switch to using `conda` and `environment.yml`
* Update dependencies (and fix the various errors this caused)
* Introduce aiscsimageio & use imageio.v3
  * Major update to the Python notebook in the 'Pixel size & dimensions' chapter

## 8 March 2023

* Update dependencies
* Dark mode support!
  * Possible thanks to [JupyterBook](https://jupyterbook.org/en/stable/intro.html) & especially [pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io/)
* Minor fixes
  * Rename `selem` to `footprint` for median filtering with scikit-image

## 15 January 2023

* Add this changelog
* Make `index.html` the main page, not `README.html`
  * Please use https://bioimagebook.github.io as the main book link (*not* https://bioimagebook.github.io/README.html)!
* Add `notranslate` class to button text and menu items
  * This aims to make Google Translate (and perhaps other translators) give more meaningful output, without mangling user interface elements.


## 20 April 2022

* First release!
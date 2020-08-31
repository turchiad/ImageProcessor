# ImageProcessor

## Overview

ImageProcessor is a general project to create basic CLI (Command-Line Interface) programs for making adjustments and edits to images.

## Image Formats

As each image format requires a different read/write basis, a different program will be developed for each filetype. It makes sense (as most image editors do), to have some sort of intermediate filetype unique to the program, which can receive all of the edits in the same format, before reorganizing them to their desire export.

As this is a very simple approach, only a program for Bitmap (`.bmp`) image files has been written.

### Bitmap Images

#### File Parsing

Bitmap (`.bmp`) images are among the most basic methods of image storage. While there is capability for compression methods, `.bmp`s are by and large binary stores of a pixel-color matrix with three headers prepended. `BitmapProcessing.py` is (as of 2020/08/31) capable of reading from and writing to a `.bmp` which does not employ the following:

* Color Palettes 
* Non-24-bit Color Depth
* Compression

As such, the application of `BitmapProcessing.py` is limited at the current time, but serves as a vehicle to experiment with and apply several image editing technniques.

#### Adjustment

`BitmapProcessing.py` is a consolidated Python3 script, which is to say that all of the functionality required for runtime is contained within it. This includes all of the image editing algorithms. As of 2020/08/31, the following image editing features have been provided.

* Brighten/Darken
  * A basic addition or subtraction of all color values by a numeral of the user's choice.
* Box Blur
  * A basic blur which adjusts each pixel to be the average of its neighbors a certain distance (of the user's choice) in both `x` and `y` away.
* Median Filter
  * A basic filter which adjusts each pixel to be the median of its neighbors a certain distance (of the user's choice) in both `x` and `y` away.
* Gaussian Blur
  * A blur which applies a Gaussian kernel (the width of which is the user's choice) in two passes (horizontal and vertical) to make each pixel the weighted average of its peers.
* Sharpen Filter
  * A filter which uses an unsharp mask to arrive at a sharpened image. This is achieved by obtaining a 'Fine' image via subtraction of a Gaussian blur from the original input and overlaying it at a fraction scale on top of the input. The user's control over this feature is still in development.

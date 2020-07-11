# Started 2020-07-11 at 4:13 P.M. by D.T.

# The Structure of a Bitmap File
## BMP Header - 14 bytes
### Filetype - 2 bytes
### Filesize - 4 bytes
### Reserved - 2 bytes
### Reserved - 2 bytes
## DIB Header - 40 bytes
### Headersize - 4 bytes
### Imagewidth - 4 bytes
### Imageheight - 4 bytes
### Colorplanes - 2 bytes
### BitsPerPixel - 2 bytes
### Compression - 4 bytes
### Imagesize - 4 bytes
### XpixelsPerMeter - 4 bytes
### YpixelsPerMeter - 4 bytes
### TotalColors - 4 bytes
### ImportantColors - 4 bytes
## Color Pallet - Variable/Optional
## BMP Content - Variable
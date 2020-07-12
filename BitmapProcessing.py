# Started 2020-07-11 at 4:13 P.M. by D.T.
# https://itnext.io/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393 is used as a reference for the structure of a Bitmap

import sys

# NOTE: Bitmaps are stored Little-Endian

# The Structure of a Bitmap File
## BMP Header - 14 bytes
### Filetype - 2 bytes
### Filesize - 4 bytes
### Reserved - 2 bytes
### Reserved - 2 bytes
### PixelDataOffset - 4 bytes
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

# If BitsPerPixel <= 8, then Color Pallet is mandatory
## TotalColors is the number of colors defined in the Pallet
## Each color shall be 4 bytes
### 3 bytes for RGB color-channels
### 4th byte reserved as 0
## Total size shall be 4 x TotalColors bytes
# If BitsPerPixel > 8, the Color Pallet is unused
## TotalColors should be set to 0

# Define Globals

BMPHEADER_SIZE = 14 #bytes
DIBHEADER_SIZE = 40 #bytes
COLORPALLET_SIZE = 0 #bytes, to be defined later

# Define Variables

## BMP Header Vars
fileType = None
fileSize = None
res1 = None
res2 = None
PixelDataOffset = None

## DIB Header Vars
headerSize = None
imageWidth = None
imageHeight = None
colorPlanes = None
bitsPerPixel = None
compression = None
imageSize = None
xPixelsPerMeter = None
yPixelsPerMeter = None
totalColors = None
importantColors = None

## Color Pallet Vars
colorPallet = None

## BMP Content Vars
bmpContent = None

def parseBytes(b):
	if len(b) > 1:
		return b
	else:
		return b

def isBitmapImage(filename):
	if filename[-4:].lower() == ".bmp":
		return True
	else:
		return False

def parseBMPHeader(h):
	# 2 bytes
	fileType = h[0:1]
	# 4 bytes
	fileSize = h[2:5]
	# 2 bytes
	res1 = h[6:7]
	# 2 bytes
	res2 = h[8:9]
	# 4 bytes
	pixelDataOffset = h[10:13]

def parseDIBHeader(h):
	# 4 bytes
	headerSize = h[0:3]
	# 4 bytes
	imageWidth = h[4:7]
	# 4 bytes
	imageHeight = h[8:11]
	# 2 bytes
	colorPlanes = h[12:13]
	# 2 bytes
	bitsPerPixel = h[14:15]
	# 4 bytes
	compression = h[16:19]
	# 4 bytes
	imageSize = h[20:23]
	# 4 bytes
	xPixelsPerMeter = h[24:27]
	# 4 bytes
	yPixelsPerMeter = h[28:31]
	# 4 bytes
	totalColors = h[32:35]
	# 4 bytes
	importantColors = h[36:39]

def parseColorPallet(h):
	#Left blank for now
	return 0

def parseBMPContent(h):
	#Remainder of the data stored as pixels
	bmpContent = h

def readBMP(filename):

	#Check if this file is a bitmap image

	if not isBitmapImage(filename):
		sys.stderr.write("Attempted to read from a file which is not a BMP. Aborting.")
		return

	#Attempt to open file

	try:
		f = open(filename,'rb')
	except:
		sys.stderr.write("Attempted to access a file which does not exist. Aborting.")
		return

	#Read contents of BMP

	data = f.read()

	#Partition Data Step 1

	BMPHeader = data[0:BMPHEADER_SIZE-1]
	DIBHeader = data[BMPHEADER_SIZE:BMPHEADER_SIZE+DIBHEADER_SIZE-1]
	
	#Parse Partitioned Data Step 1

	parseBMPHeader(BMPHeader)
	parseDIBHeader(DIBHeader)

	#Contingent on the DIB Header being parsed correctly
	if bitsPerPixel > 8 and totalColors == 0:
		COLORPALLET_SIZE = 0
	elif bitsPerPixel <= 8 and totalColors == 0:
		sys.stderr.write("BitsPerPixel <= 8 and TotalColors > 0 resulting in an inconsistency. Aborting.")
		return
	else:
		COLORPALLET_SIZE = 4 * totalColors


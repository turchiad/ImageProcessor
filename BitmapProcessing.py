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
pixelDataOffset = None

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

## Color Pallet Array
colorPallet = None

## BMP Content Vars
bmpContent = None

# Define Help String

helpString = """usage: python /path/to/BitmapProcessing.py [options] [filename]
	-?: Show usage for this script"""

# Define option checks
debugCheck = 0

# The purpose of printDebug() is to provide an overview of the script's state
def printDebug():

	#BMP Header Vars
	print("BMP Header Data:")
	print("File Type: " + str(fileType))
	print("File Size: " + str(fileSize))
	print("Reserved Byte #1: " + str(res1))
	print("Reserved Byte #2: " + str(res2))
	print("PixelDataOffset: " + str(pixelDataOffset))

	#DIB Header vars
	print("\nDIB Header Data:")
	print("Header Size: " + str(headerSize))
	print("Image Width: " + str(imageWidth))
	print("Image Height: " + str(imageHeight))
	print("Color Planes: " + str(colorPlanes))
	print("Bites Per Pixel: " + str(bitsPerPixel))
	print("Compression: " + str(compression))
	print("Image Size: " + str(imageSize))
	print("X-Pixels Per Meter: " + str(xPixelsPerMeter))
	print("Y-Pixels Per Meter: " + str(yPixelsPerMeter))
	print("Total Colors: " + str(totalColors))
	print("Important Colors: " + str(importantColors))


def parseBytes(b):
	return int.from_bytes(b,'little')

def isBitmapImage(filename):
	if filename[-4:].lower() == ".bmp":
		return True
	else:
		return False

def parseBMPHeader(h):

	# Define globals
	global fileType, fileSize, res1, res2, pixelDataOffset

	# 2 bytes
	fileType = parseBytes(h[0:1])
	# 4 bytes
	fileSize = parseBytes(h[2:5])
	# 2 bytes
	res1 = parseBytes(h[6:7])
	# 2 bytes
	res2 = parseBytes(h[8:9])
	# 4 bytes
	pixelDataOffset = parseBytes(h[10:13])

def parseDIBHeader(h):

	# Define globals

	global headerSize, imageWidth, imageHeight, colorPlanes, bitsPerPixel, \
	compression, imageSize, xPixelsPerMeter, yPixelsPerMeter, totalColors, importantColors

	# 4 bytes
	headerSize = parseBytes(h[0:3])
	# 4 bytes
	imageWidth = parseBytes(h[4:7])
	# 4 bytes
	imageHeight = parseBytes(h[8:11])
	# 2 bytes
	colorPlanes = parseBytes(h[12:13])
	# 2 bytes
	bitsPerPixel = parseBytes(h[14:15])
	# 4 bytes
	compression = parseBytes(h[16:19])
	# 4 bytes
	imageSize = parseBytes(h[20:23])
	# 4 bytes
	xPixelsPerMeter = parseBytes(h[24:27])
	# 4 bytes
	yPixelsPerMeter = parseBytes(h[28:31])
	# 4 bytes
	totalColors = parseBytes(h[32:35])
	# 4 bytes
	importantColors = parseBytes(h[36:39])

def parseColorPallet(h):
	#Number of Rows/Colors in the Pallet
	numRows= len(h)/4

	#Initialize empty array
	colorPallet = [[None for i in range(4)] for j in range(numRows)]

	for j in range(numRows):
		for i in range(4):
			colorPallet[i][j] = parseBytes(h[j*4+i])


def parseBMPContent(h):
	#Remainder of the data stored as pixels
	bmpContent = h

	#Data shall be organized as follows:
	## BytesPerPixel = BitsPerPixel / 4
	## HorizontalLength = ImageWidth * BytesPerPixel
	## VerticalLength = ImageHeight * BytesPerPixel
	## There must be a pixel data structure to hand each pixel.

def readBMP(filename):

	#Check if this file is a bitmap image

	if not isBitmapImage(filename):
		sys.stderr.write("Attempted to read from a file which is not a BMP. Aborting.\n")
		return

	#Attempt to open file

	try:
		f = open(filename,'rb')
	except:
		sys.stderr.write("Attempted to access a file which does not exist. Aborting.\n")
		return

	#Read contents of BMP

	data = f.read()

	#Partition Data Step 1

	BMPHeader = data[0:BMPHEADER_SIZE-1]
	DIBHeader = data[BMPHEADER_SIZE:BMPHEADER_SIZE+DIBHEADER_SIZE-1]
	
	#Parse Partitioned Data Step 1

	parseBMPHeader(BMPHeader)
	parseDIBHeader(DIBHeader)

	return

	#Contingent on the DIB Header being parsed correctly

	#If BitsPerPixel is more than 8 (and therefore totalColors = 0)
	if bitsPerPixel > 8 and totalColors == 0:
		COLORPALLET_SIZE = 0
	#If BitsPerPixel is less than or equal to 8, but totalColors is still 0 (should not happen)
	elif bitsPerPixel <= 8 and totalColors == 0:
		sys.stderr.write("BitsPerPixel <= 8 and TotalColors > 0 resulting in an inconsistency. Aborting.\n")
		return
	#If BitsPerPixel is less than or equal to 8 (and therefore totalColors > 0)
	else:
		COLORPALLET_SIZE = 4 * totalColors

	#Partition Data Step 2

	ColorPallet = data[BMPHEADER_SIZE+DIBHEADER_SIZE:BMPHEADER_SIZE+DIBHEADER_SIZE+COLORPALLET_SIZE-1]
	BMPContent = data[BMPHEADER_SIZE+DIBHEADER_SIZE+COLORPALLET_SIZE:]

	#Parse Partitioned Data Step 2

	parseColorPallet(ColorPallet)
	parseBMPContent(BMPContent)


# Main Runtime

## In case this script is called without arguments
if len(sys.argv) <= 1:
	sys.stderr.write("Please refer to instructions for how to run this script. Type:\n\npython BitmapProcessing.py -?\n\n")
	sys.exit()
## In case the user requests instructions
### This must be located here because it is the only option which requries no filename
elif "-?" in sys.argv:
	print(helpString)
	sys.exit()
## In case the user has provided multiple filenames. Exactly one is required.
elif len(list(x for x in sys.argv if not x.startswith("-"))) > 2:
	sys.stderr.write("Multiple filenames have been provided. Please provide exactly one non-option argument. See -? for help.\n")
	sys.exit()
## In case the user has not provided a filename. Exactly one is require
elif len(list(x for x in sys.argv if not x.startswith("-"))) <= 1:
	sys.stderr.write("No filenames have been provided. Please provide exactly one non-option argument. See -? for help.\n")
	sys.exit()

# If no override states have been encountered proceed with runtime

## Option Handling

# If -debug is on, then provide extra print statements wherever necessary
if "-debug" in sys.argv:
	debugCheck = 1


# The filename shall be the second non-option element of the arguments
filename = list((x for x in sys.argv if not x.startswith("-")))[1]


if debugCheck:
	print("\n--INITIAL PARAMETERS PRINT--\n")
	printDebug()

readBMP(filename)

if debugCheck:
	print("\n--POST READ PRINT--\n")
	printDebug()




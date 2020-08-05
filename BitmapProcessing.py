# Started 2020-07-11 at 4:13 P.M. by D.T.
# https://itnext.io/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393 is used as a reference for the structure of a Bitmap

import sys, copy, math

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

BMPHEADER_SIZE = 14 # bytes
DIBHEADER_SIZE = 40 # bytes
COLORPALLET_SIZE = 0 # bytes, to be defined later

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
pixelData = None

# Define Help String

helpString = """usage: python /path/to/BitmapProcessing.py [options] [inputFilename]
	-?: Show usage for this script
	-debug: Provide verbose debugging info during runtime
	-o=[filename]: Output the file read to the inputFilename provided here"""

# Define option checks
debugCheck = 0
outputCheck = 0

# The purpose of printDebug() is to provide an overview of the script's state
def printDebug():

	# BMP Header Vars
	print("BMP Header Data:")
	print("File Type: " + str(fileType))
	print("File Size: " + str(fileSize))
	print("Reserved Byte # 1: " + str(res1))
	print("Reserved Byte # 2: " + str(res2))
	print("PixelDataOffset: " + str(pixelDataOffset))

	# DIB Header vars
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

	# Color Pallet vars
	print("\nColor Pallet Data:")
	if colorPallet == None:
		print("The Color Pallet has not been evaluated.")
	# Short circuiting will ensure this does not run on None
	elif len(colorPallet) == 0:
		print("The Color Pallet is not used.")
	else:

		# Color Pallet Rows
		cpRows = len(colorPallet)
		# Color Pallet Cols
		cpCols = len(colorPallet[0])

		# Print the 2D Array
		print("The Color Pallet has " + str(cpRows) + " rows")
		for i in range(cpRows):
			print("Row " + str(i) + ": ",end="")
			for j in range(cpCols):
				print(str(colorPallet[i][j]),end="")
				if j < cpCols-1:
					print(",",end="")
			print()

	# bmpContent vars
	print("\nBMP Content/Pixel Data:")
	if bmpContent == None:
		print("BMP Content has not yet been evaluated.")
	else:
		print("BMP Content has been loaded with " + str(len(bmpContent)) + " bytes.")

# Input Processing Functions

def parseBytes(b):
	if isinstance(b,int):
		return b
	elif not isinstance(b, bytes):
		sys.stderr.write("Attempted to process non-byte data into integers. Aborting.\n")
		sys.exit()
	else:
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
	fileType = parseBytes(h[0:2])
	# 4 bytes
	fileSize = parseBytes(h[2:6])
	# 2 bytes
	res1 = parseBytes(h[6:8])
	# 2 bytes
	res2 = parseBytes(h[8:10])
	# 4 bytes
	pixelDataOffset = parseBytes(h[10:14])

def parseDIBHeader(h):

	# Define globals

	global headerSize, imageWidth, imageHeight, colorPlanes, bitsPerPixel, \
	compression, imageSize, xPixelsPerMeter, yPixelsPerMeter, totalColors, importantColors

	# 4 bytes
	headerSize = parseBytes(h[0:4])
	# 4 bytes
	imageWidth = parseBytes(h[4:8])
	# 4 bytes
	imageHeight = parseBytes(h[8:12])
	# 2 bytes
	colorPlanes = parseBytes(h[12:14])
	# 2 bytes
	bitsPerPixel = parseBytes(h[14:16])
	# 4 bytes
	compression = parseBytes(h[16:20])
	# 4 bytes
	imageSize = parseBytes(h[20:24])
	# 4 bytes
	xPixelsPerMeter = parseBytes(h[24:28])
	# 4 bytes
	yPixelsPerMeter = parseBytes(h[28:32])
	# 4 bytes
	totalColors = parseBytes(h[32:36])
	# 4 bytes
	importantColors = parseBytes(h[36:40])

def parseColorPallet(h):

	# Define Globals
	global colorPallet

	# Number of Rows/Colors in the Pallet
	numRows= int(len(h)/4)

	# Print numRows if debug is checked.
	if debugCheck:
		print("\n--FROM parseColorPallet()--")
		print("Number of Color Pallet Rows: " + str(numRows) + "\n")

	# Initialize empty array
	colorPallet = [[None for i in range(4)] for j in range(numRows)]

	counter = 0

	for j in range(numRows):
		for i in range(4):
			colorPallet[i][j] = h[counter]
			counter += 1


	# Print the 2D size of colorPallet if debug is checked.
	if debugCheck:
		print("\n--FROM parseColorPallet()--")
		ySize = len(colorPallet)
		if ySize > 0:
			xSize = len(colorPallet[0])
			print("colorPallet is: [" + str(xSize) + " x " + str(ySize) + "]\n")
		else:
			print("colorPallet is: [0 x 0]\n")

def parseBMPContent(h):

	# Define Globals
	global bmpContent, pixelData

	# Remainder of the data stored as pixels
	bmpContent = h

	# Initialize pixelData as a [Height][Width][Pixel] array
	# Currently this only functions for 24-bit color depth.
	# I will have to implement a 'pixel' object to complete this properly.

	pixelSize = int(bitsPerPixel/8)

	pixelData = [[[None for cell in range(pixelSize)] for col in range(imageWidth)] for row in range(imageHeight)]

	counter = 0

	for i in range(imageHeight):
		for j in range(imageWidth):
			for k in range(pixelSize):
				pixelData[i][j][k] = bmpContent[counter]
				counter += 1

def readBMP(inputFilename):

	# Check if this file is a bitmap image

	if not isBitmapImage(inputFilename):
		sys.stderr.write("Attempted to read from a file which is not a BMP. Aborting.\n")
		sys.exit()

	# Attempt to open file

	try:
		f = open(inputFilename,'rb')
	except:
		sys.stderr.write("Attempted to access a file which does not exist. Aborting.\n")
		sys.exit()

	# Read contents of BMP

	data = f.read()

	# Partition Data Step 1

	BMPHeader = data[0:BMPHEADER_SIZE]
	DIBHeader = data[BMPHEADER_SIZE:BMPHEADER_SIZE+DIBHEADER_SIZE]
	
	# Parse Partitioned Data Step 1

	parseBMPHeader(BMPHeader)
	parseDIBHeader(DIBHeader)

	# Contingent on the DIB Header being parsed correctly

	# Must define COLORPALLET_SIZE as a global because it is evaluated here.
	global COLORPALLET_SIZE

	# If BitsPerPixel is more than 8 (and therefore totalColors = 0)
	if bitsPerPixel > 8 and totalColors == 0:
		COLORPALLET_SIZE = 0
	# If BitsPerPixel is less than or equal to 8, but totalColors is still 0 (should not happen)
	elif bitsPerPixel <= 8 and totalColors == 0:
		sys.stderr.write("BitsPerPixel <= 8 and TotalColors > 0 resulting in an inconsistency. Aborting.\n")
		sys.exit()
		return
	# If BitsPerPixel is less than or equal to 8 (and therefore totalColors > 0)
	else:
		COLORPALLET_SIZE = 4 * totalColors


	# Quality Check
	if BMPHEADER_SIZE + DIBHEADER_SIZE + COLORPALLET_SIZE != pixelDataOffset:
		sys.stderr.write("WARNING: pixelDataOffset does not match ColorPallet information. This BMP file has not been properly constructed.\n")

	# Partition Data Step 2

	ColorPallet = data[BMPHEADER_SIZE+DIBHEADER_SIZE:BMPHEADER_SIZE+DIBHEADER_SIZE+COLORPALLET_SIZE]
	BMPContent = data[BMPHEADER_SIZE+DIBHEADER_SIZE+COLORPALLET_SIZE:]

	# Parse Partitioned Data Step 2

	parseColorPallet(ColorPallet)
	parseBMPContent(BMPContent)


# Output Processing Functions

def printBMPHeader():

	# 2 bytes
	b = fileType.to_bytes(2,'little')

	# 6 bytes
	b += fileSize.to_bytes(4,'little')

	# 8 bytes
	b += res1.to_bytes(2,'little')

	# 10 bytes
	b += res2.to_bytes(2,'little')

	# 14 bytes
	b += pixelDataOffset.to_bytes(4,'little')

	return b


def printDIBHeader():

	# 4 bytes
	b = headerSize.to_bytes(4,'little')

	# 8 bytes
	b += imageWidth.to_bytes(4,'little')

	# 12 bytes
	b += imageHeight.to_bytes(4,'little')

	# 14 bytes
	b += colorPlanes.to_bytes(2,'little')

	# 16 bytes
	b += bitsPerPixel.to_bytes(2,'little')

	# 20 bytes
	b += compression.to_bytes(4,'little')

	# 24 bytes
	b += imageSize.to_bytes(4,'little')

	# 28 bytes
	b += xPixelsPerMeter.to_bytes(4,'little')

	# 32 bytes
	b += yPixelsPerMeter.to_bytes(4,'little')

	# 36 bytes
	b += totalColors.to_bytes(4,'little')

	# 36 bytes
	b += importantColors.to_bytes(4,'little')

	return b

def printBMPContent():

	# Initialize empty bytes object

	b = b''

	count = 0

	for row in pixelData:
		for col in row:
			count += 1
			if count % 100 == 0:
				print("Progress: " + "{:.2f}".format(count / (imageWidth*imageHeight)*100))
			for i in col:
				b += i.to_bytes(1,'little')

	return b

# Image Filtering

def isImageLoaded():
	if pixelData == None or len(pixelData) == 0:
		sys.stderr.write("Error when editing image: pixelData is empty. Aborting.\n")
		sys.exit(0)


## The purpose of this function is to take pixelData and modify the values
## by intensity * 10, to a maximum of 255.
def brighten(intensity):

	global pixelData

	# Check if pixelData is loaded
	isImageLoaded()

	# Provide function for mapping over pixelData
	def increaseBy(val):
		return val + 10 * intensity if val + 10 * intensity <= 255 else 255

	pixelData = list(map( \
		lambda row: list(map( \
		lambda col: list(map( \
		increaseBy, col)), row)), pixelData))

## The purpose of this function is to take pixelData and apply a box blur to it
## This is to say that every element of pixelData shall become the average of itself and its
## peers within dist of the origin point such that boxBlur(0) returns the exact same image
## and boxBlur(imageHeight if imageHeight > imageWidth else imageWidth) returns an image
## which is all the same color.
def boxBlur(dist):

	global pixelData

	# Edge case
	if dist == 0:
		return

	# Check if pixelData is loaded
	isImageLoaded()


	# Check if dist is in the right format.
	# Short circuiting will prevent the dist.is_integer from executing, averting a crash
	if isinstance(dist,float) and dist.is_integer() and not isinstance(dist,int):
		sys.stderr.write("Error: non-integer value provided as an argument for boxBlur.\n")

	# We must create a reference array so we don't pull from blurred values
	ref = copy.deepcopy(pixelData)

	# Get upper boundaries of image dimensions for edge cases
	rowBound = len(ref)
	colBound = len(ref[0])

	# Apply box blur
	for row in range(len(pixelData)):
		for col in range(len(pixelData[row])):
			for color in range(len(pixelData[row][col])):
				# Initialize the sum & n for the average
				colorSum = 0
				n = 0

				# Iterate from -dist to dist (min 0, max rowBound)
				startRow = row - dist if row - dist > 0 else 0
				startCol = col - dist if col - dist > 0 else 0
				endRow = row + dist if row + dist + 1 < rowBound else rowBound
				endCol = col + dist if col + dist + 1 < colBound else colBound 

				# Add elements of sum
				for i in range(startRow,endRow):
					for j in range(startCol, endCol):
						try:
							colorSum += ref[i][j][color]
							n += 1
						except:
							sys.stderr.print("Error: attempted to access non-existent value in box blur. Aborting.\n")
							sys.exit()

				colorAve = colorSum / n
				pixelData[row][col][color] = int(colorAve) if colorAve >= 0 and colorAve <= 255 else 255 if colorAve > 255 else 0

## The purpose of this function is to take pixelData and apply a median filter to it.
## This is to say that every element of pixelData should be the median of itself and
## its peers within dist.
def medianFilter(dist):

	global pixelData

	# Edge case
	if dist == 0:
		return

	# Check if pixelData is loaded
	isImageLoaded()


	# Check if dist is in the right format.
	# Short circuiting will prevent the dist.is_integer from executing, averting a crash
	if isinstance(dist,float) and dist.is_integer() and not isinstance(dist,int):
		sys.stderr.write("Error: non-integer value provided as an argument for boxBlur.\n")

	# We must create a reference array so we don't pull from blurred values
	ref = copy.deepcopy(pixelData)

	# Get upper boundaries of image dimensions for edge cases
	rowBound = len(ref)
	colBound = len(ref[0])

	count = 0

	# Apply median filter
	for row in range(len(pixelData)):
		for col in range(len(pixelData[row])):
			count += 1
			if count % 100 == 0:
				print("Progress: " + "{:.2f}".format(count / (imageWidth*imageHeight)*100))
			for color in range(len(pixelData[row][col])):
				# Initialize the median
				colorMed = []

				# Iterate from -dist to dist (min 0, max rowBound)
				startRow = row - dist if row - dist > 0 else 0
				startCol = col - dist if col - dist > 0 else 0
				endRow = row + dist if row + dist + 1 < rowBound else rowBound
				endCol = col + dist if col + dist + 1 < colBound else colBound 

				# Add elements of sum
				for i in range(startRow,endRow):
					for j in range(startCol, endCol):
						try:
							colorMed.append(ref[i][j][color])
						except:
							sys.stderr.print("Error: attempted to access non-existent value in box blur. Aborting.\n")
							sys.exit()

				colorMed.sort()
				pixelData[row][col][color] = colorMed[math.ceil(len(colorMed) / 2 - 1)]

def printBMP(outputFilename):

	# Check if this file is a bitmap image

	if not isBitmapImage(outputFilename):
		sys.stderr.write("WARNING: Printing to a file without a .bmp extension.\n")

	# Attempt to open file

	try:
		f = open(outputFilename,'wb')
	except:
		sys.stderr.write("Error when opening file to write to. Aborting.\n")
		sys.exit()

	# Initialize the byte string we will be constructing to print to the output file.

	outputBytes = b''

	outputBytes += printBMPHeader()
	outputBytes += printDIBHeader()
	# outputBytes += printColorPallet()
	outputBytes += printBMPContent()

	# Print to output file
	f.write(outputBytes)
	f.close()


# Main Runtime

## In case this script is called without arguments
if len(sys.argv) <= 1:
	sys.stderr.write("Please refer to instructions for how to run this script. Type:\n\npython BitmapProcessing.py -?\n\n")
	sys.exit()
## In case the user requests instructions
### This must be located here because it is the only option which requries no inputFilename
elif "-?" in sys.argv:
	print(helpString)
	sys.exit()
## In case the user has provided multiple filenames. Exactly one is required.
elif len(list(x for x in sys.argv if not x.startswith("-"))) > 2:
	sys.stderr.write("Multiple filenames have been provided. Please provide exactly one non-option argument. See -? for help.\n")
	sys.exit()
## In case the user has not provided a inputFilename. Exactly one is require
elif len(list(x for x in sys.argv if not x.startswith("-"))) <= 1:
	sys.stderr.write("No filenames have been provided. Please provide exactly one non-option argument. See -? for help.\n")
	sys.exit()

# If no override states have been encountered proceed with runtime

## Option Handling

# If -debug is on, then provide extra print statements wherever necessary
if "-debug" in sys.argv:
	debugCheck = 1

# Handling output tags
outputTag = [x for x in sys.argv if x.startswith("-o")]
# If -o is provided twice
if len(outputTag) > 1:
	sys.stderr.write("Multiple filenames have been provided for the output tag -o. Please provide only one -o option.\n")
	sys.exit()
# If -o is provided correctly
elif len(outputTag) == 1:
	outputCheck = 1
	# Isolate -o option
	outputTag = outputTag[0]
	# Check if -o option is configured properly
	if "=" not in outputTag:
		sys.stderr.write("-o output option has not been configured properly. See -? for help.\n")
		sys.exit()
	outputFilename = outputTag[outputTag.index("=")+1:]
	if len(outputFilename) == 0:
		sys.stderr.write("-o output option has not been configured properly. See -? for help.\n")
		sys.exit()

# The inputFilename shall be the second non-option element of the arguments
inputFilename = list(x for x in sys.argv if not x.startswith("-"))[1]

if debugCheck:
	print("\n--INITIAL PARAMETERS PRINT--\n")
	printDebug()

readBMP(inputFilename)

if debugCheck:
	print("\n--POST READ PRINT--\n")
	printDebug()

###
###
# ANY PROCESSING TO BE DONE PER THE OPTIONS TAGS
###
###

# Handling modifier tags
modTags = [x for x in sys.argv if x.startswith("-m")]

for modTag in modTags:
	# Check the that modifier is written properly
	if "=" not in modTag:
		sys.stderr.write("-m modifier option has not been configured properly. See -? for help.\n")
		sys.exit()
	# Modifier inidcator
	modType = modTag[modTag.index("=")+1:].lower()

	# Handling modifier indicator by type

	# Median Filter

	if modType.startswith("mf"):

		modTypeIndicator = "mf"

		# Check that the box blur modifier has an argument:
		modTypeArgs = modType[len(modTypeIndicator):]

		modTypeTest1 = modTypeArgs.startswith("[")
		modTypeTest2 = modTypeArgs.endswith("]")
		modTypeTest3 = modTypeArgs[1:-1].isdecimal()

		if not (modTypeTest1 and modTypeTest2 and modTypeTest3):
			sys.stderr.write("-m modifier bb has not been configured properly. See -? for help.\n")
			sys.exit()

		# Handle arguments
		
		# Cast brightness intensity to int
		arg = None
		try:
			arg = int(modTypeArgs[1:-1])
		except:
			sys.stderr.write("Unexpected error. Non-decimal arguments have been provided to modifier option. Configuration precheck failed. Aborting. \n")
			sys.exit()

		# If nothing has failed so far:
		medianFilter(arg)

	# Box Blur

	elif modType.startswith("bb"):

		modTypeIndicator = "bb"

		# Check that the box blur modifier has an argument:
		modTypeArgs = modType[len(modTypeIndicator):]

		modTypeTest1 = modTypeArgs.startswith("[")
		modTypeTest2 = modTypeArgs.endswith("]")
		modTypeTest3 = modTypeArgs[1:-1].isdecimal()

		if not (modTypeTest1 and modTypeTest2 and modTypeTest3):
			sys.stderr.write("-m modifier bb has not been configured properly. See -? for help.\n")
			sys.exit()

		# Handle arguments
		
		# Cast brightness intensity to int
		arg = None
		try:
			arg = int(modTypeArgs[1:-1])
		except:
			sys.stderr.write("Unexpected error. Non-decimal arguments have been provided to modifier option. Configuration precheck failed. Aborting. \n")
			sys.exit()

		# If nothing has failed so far:
		boxBlur(arg)

	# Brighten

	elif modType.startswith("b"):

		modTypeIndicator = "b"

		# Check that the box blur modifier has an argument:
		modTypeArgs = modType[len(modTypeIndicator):]

		modTypeTest1 = modTypeArgs.startswith("[")
		modTypeTest2 = modTypeArgs.endswith("]")
		modTypeTest3 = modTypeArgs[1:-1].isdecimal()

		if not (modTypeTest1 and modTypeTest2 and modTypeTest3):
			sys.stderr.write("-m modifier bb has not been configured properly. See -? for help.\n")
			sys.exit()

		# Handle arguments
		
		# Cast brightness intensity to int
		arg = None
		try:
			arg = int(modTypeArgs[1:-1])
		except:
			sys.stderr.write("Unexpected error. Non-decimal arguments have been provided to modifier option. Configuration precheck failed. Aborting. \n")
			sys.exit()

		# If nothing has failed so far:
		brighten(arg)

# Outputting

# Conditional on -o
if outputCheck:
	print("Entering print.")
	printBMP(outputFilename)




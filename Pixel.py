# Started 2020-07-19 at 11:58 A.M. by D.T.

import sys

# The Structure of a BMP Pixel
## R - Red Value
## G - Green Value
## B - Blue Value

## In the interest of speed, there will be as few instance variables as possible.


# Parent Class

class Pixel:

	def __init__(self, R, G, B):
		self.R = R
		self.G = G
		self.B = B

	def __str__(self):
		return "[" + str(self.R) + "," + str(self.G) + "," + str(self.B) + "]"


# Inherit Pixel

class BMPPixel(Pixel):

	# Class Variables

	## A Dictionary which infers the size of R,G, and B from the size of Raw
	### 8 bits is to be handled separately
	### 16 bits -> 5 bits
	### 24 bits -> 8 bits
	### 32 bits -> 10 bits
	### 64 bits -> 21 bits
	sizeDict = {8:2,}

	def __init__(self, raw):
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

	def __init__(self, R, G, B):
		super().__init__(R, G, B)
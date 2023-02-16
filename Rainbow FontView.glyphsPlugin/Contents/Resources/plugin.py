# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class RainbowFontView(GeneralPlugin):

	# Set name of plugin
	@objc.python_method
	def settings(self):
		self.name = "Rainbow FontView"
		

	# Add plugin in "File" Menu, and add callback.
	@objc.python_method
	def start(self):
		newMenuItem = NSMenuItem(self.name, self.enableFilter)
		Glyphs.addCallback(self.updateGlyphOrder, UPDATEINTERFACE)
		Glyphs.menu[FILE_MENU].append(newMenuItem)

	# Callback trigger by triggering Menu item
	@objc.python_method
	def enableFilter(self, sender=None):
		self.font = Glyphs.currentDocument.font
		masterID = self.font.selectedFontMaster.id

		checkLayerColor = {}
		for glyph in self.font.glyphs:
			color = glyph.layers[masterID].color
			checkLayerColor[color]=''
		if len(checkLayerColor) == 1 and checkLayerColor[None]=="":
			Message("It seems you didn't set\nLayer Color for Selected Master\nTo set a Layer Color press :\n[Right Click + Option]", title='No Layer Color Set', OKButton=None)

		# When activated for the first time, create tempData with True
		if not Glyphs.font.tempData['filterEnable']:
			Glyphs.font.tempData['filterEnable'] = False

		# Because this plugin need a "glyphOrder" custom parameter to work, if it's missing, add one empty.
		if not Glyphs.font.customParameters["glyphOrder"]:
			Glyphs.font.customParameters["glyphOrder"] = ()

		# If Filter is enable, disable it
		if Glyphs.font.tempData['filterEnable'] == True:
			Glyphs.font.tempData['filterEnable'] = False

			# Temp solution to enable/disable custom parameter
			i = -1
			for cp in Glyphs.font.customParameters:
				i += 1
				if cp.name == "glyphOrder":
					break
			Glyphs.font.customParameters[i].setActive_(False)
			#Message("FontView Layer Color Filter ❌", title='Alert', OKButton=None)

		# If Filter is disable, enable it
		else :
			Glyphs.font.tempData['filterEnable'] = True

			# Update glyphOrder
			self.GenerateLayerColorGlyphOrder()
			Glyphs.font.customParameters["glyphOrder"] = self.code

			# Temp solution to eable/disable custom parameter
			
			i = -1
			for cp in Glyphs.font.customParameters:
				i += 1
				if cp.name == "glyphOrder":
					break
			Glyphs.font.customParameters[i].setActive_(True)
			#Message("FontView Layer Color Filter ✅", title='Alert', OKButton=None)

	# Update glyphOrder based on layer color of Selected Master
	@objc.python_method
	def updateGlyphOrder(self, sender):

		# If filter is Enable
		if Glyphs.font.tempData['filterEnable'] == True:
			self.font = Glyphs.currentDocument.font

			# Save Selected Master
			if not self.font.tempData['selectedMaster']:
				self.font.tempData['selectedMaster'] = self.font.selectedFontMaster.id

			# If no data related to Layer Color saved, save Color Layer data of Selected Master
			if not self.font.tempData['saveColorLayers']:
				self.GenerateLayerColorGlyphOrder()
				self.font.tempData['saveColorLayers'] = self.colorLabels	

			# If user is in FontView
			if self.font.currentTab == None:
				print("We are in FontView")

				# If Selected Master has been changed
				if self.font.tempData['selectedMaster'] != self.font.selectedFontMaster.id:
					print("Master Changed")
					self.font.tempData['selectedMaster'] = self.font.selectedFontMaster.id

					# Update Layer Color data and update "glyphOrder" custom parameter
					self.GenerateLayerColorGlyphOrder()
					self.font.customParameters["glyphOrder"] = self.code

				# If Selected Master has not been changed, but a layer is selecyed
				elif self.font.selectedLayers:
					colorLayerDic = self.font.tempData['saveColorLayers']
					for layer in self.font.selectedLayers:
						color = layer.color
						glyphName = layer.parent.name
						initValue = [key for key in colorLayerDic if glyphName in colorLayerDic[key]]
						
						print(f"Layer Color : {color}")
						print(f"Previous Color : {initValue}")
						print(colorLayerDic)
						# If Selected Layer has a Layer Color
						if color != None:
							# If Layer Color not already in glyphOrder, update glyphOrder
							if color not in colorLayerDic:
								print("New color added in FontView")
								self.GenerateLayerColorGlyphOrder()
								self.font.customParameters["glyphOrder"] = self.code
								break
    
						

							# If Layer Color has been modified, update glyphOrder
							elif glyphName not in colorLayerDic[color]:
								print("Color Changed")
								self.GenerateLayerColorGlyphOrder()
								self.font.customParameters["glyphOrder"] = self.code
								break

						if color == None and initValue[0] != 13 :
							print("AIE")
							self.GenerateLayerColorGlyphOrder()
							self.font.customParameters["glyphOrder"] = self.code
							break
						




	# Return :
	# self.code 	    -> List object with code to be insert in glyphOrder
	# self.colorLabels  -> Dic object with Layer Color Data of Selected Master
	@objc.python_method
	def GenerateLayerColorGlyphOrder(self):
		colorMeaning = {'0': '🚨 Red', '1': '🦊 Orange', '2': '🪵 Brown', '3': '🌼 Yellow', '4': '🍀 Light green', '5': '🫑 Dark green', '6': '💎 Light blue', '7': '🌀 Dark blue', '8': '🔮 Purple', '9': '🌺 Magenta', '10': '🏐 Light Gray', '11': '🎱 Charcoal'}
		
		masterID = self.font.selectedFontMaster.id

		# Temp solution to eable/disable custom parameter
		i = -1
		for cp in self.font.customParameters:
			i += 1
			if cp.name == "glyphOrder":
				break
		self.font.customParameters[i].setActive_(False)

		self.colorLabels = {}
		for glyph in self.font.glyphs:
			color = glyph.layers[masterID].color
			if color not in self.colorLabels:
				self.colorLabels[color] = []
			self.colorLabels[color].append(glyph.name)


		if None in self.colorLabels:
			self.colorLabels[13] = self.colorLabels.pop(None)

		myKeys = list(self.colorLabels.keys())
		myKeys.sort()
		self.colorLabels = {i: self.colorLabels[i] for i in myKeys}
		# if 13 in self.colorLabels:
		# 	self.colorLabels["Not set"] = self.colorLabels.pop(13)

		self.code = ["#Color Layer Filter:"]
		for color, glyph in self.colorLabels.items():
			if str(color) in colorMeaning.keys():
				self.code.append(f"**{colorMeaning[str(color)]}**")
				self.code.extend(glyph)
			else:
				self.code.append(f"**No Color**")
				self.code.extend(glyph)

		# Update Layer Color Data in font.tempData
		self.font.tempData['saveColorLayers'] = self.colorLabels
		self.font.customParameters[i].setActive_(True)

		return self.code, self.colorLabels

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

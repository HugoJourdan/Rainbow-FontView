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
import re
import os
import codecs
from collections import OrderedDict

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

		self.colorMeaning, self.order = self.mapKeys(self.getKeyFile())

		# When activated for the first time, create tempData with True
		if not Glyphs.font.tempData['filterEnable']:
			Glyphs.font.tempData['filterEnable'] = False

		if not self.font.userData["hugojourdan.RainbowFontView.labelUsed"]:
			self.font.userData["hugojourdan.RainbowFontView.labelUsed"] = "Layer"

		# Warning message
		color_set = set()
		label_used = self.font.userData["hugojourdan.RainbowFontView.labelUsed"]
		for glyph in self.font.glyphs:
			if label_used =="Layer":
				color_set.add(glyph.layers[masterID].color)
			else:
				color_set.add(glyph.color)
		if len(color_set) == 1 and None in color_set:
			if label_used =="Layer":
				message = f"It seems you didn't set\nLayer Color for Selected Master\nTo set a Layer Color press :\n[Right Click + Option]"
			else:
				message = f"It seems you didn't set\nGlyph Color in your project\nTo set a Glyph Color press :\n[Right Click]"
			Message(message, title=f'No {label_used} Color Set', OKButton=None)
		
		# Because this plugin need a "glyphOrder" custom parameter to work, if it's missing, add one empty.
		if not Glyphs.font.customParameters["glyphOrder"]:
			Glyphs.font.customParameters["glyphOrder"] = ()

		# If Filter is enable, disable it
		if Glyphs.font.tempData['filterEnable'] == True:
			Glyphs.font.tempData['filterEnable'] = False

			# Temp solution to enable/disable custom parameter
			for i, cp in enumerate(Glyphs.font.customParameters):
				if cp.name == "glyphOrder":
					cp.setActive_(False)
					break
			Glyphs.font.customParameters[i].setActive_(False)

		# If Filter is disable, enable it
		else :
			Glyphs.font.tempData['filterEnable'] = True

			# Update glyphOrder
			self.UpdateGlyphOrder()
			#Glyphs.font.customParameters["glyphOrder"] = self.code

			# Temp solution to eable/disable custom parameter
			for i, cp in enumerate(Glyphs.font.customParameters):
				if cp.name == "glyphOrder":
					cp.setActive_(False)
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
				self.UpdateGlyphOrder()
				

			# If user is in FontView
			if self.font.currentTab == None:
				###print("We are in FontView")

				# If Selected Master has been changed
				if self.font.tempData['selectedMaster'] != self.font.selectedFontMaster.id:
					self.font.tempData['selectedMaster'] = self.font.selectedFontMaster.id

					# Update Layer Color data and update "glyphOrder" custom parameter
					self.UpdateGlyphOrder()
					#self.font.customParameters["glyphOrder"] = self.code

				# If Selected Master has not been changed, but a layer is selecyed
				elif self.font.selectedLayers:
					colorLayerDic = self.font.tempData['saveColorLayers']
					glyphs_to_update = set()
					label_used = self.font.userData["hugojourdan.RainbowFontView.labelUsed"]
					for layer in self.font.selectedLayers:
						if label_used == "Glyph":
							color = layer.parent.color
						else:
							color = layer.color
						glyph_name = layer.parent.name
						if color is not None:
							if color not in colorLayerDic:
								glyphs_to_update.add(glyph_name)
							elif glyph_name not in colorLayerDic[color]:
								glyphs_to_update.add(glyph_name)
						elif glyph_name not in colorLayerDic.get(13, []):
							glyphs_to_update.add(glyph_name)
					if glyphs_to_update:
						self.UpdateGlyphOrder()
						#self.font.customParameters["glyphOrder"] = self.code


	# Return :
	# self.code 	    -> List object with code to be insert in glyphOrder
	# self.colorLabels  -> Dic object with Color Label Data of Selected Master
	@objc.python_method
	def UpdateGlyphOrder(self):

		# Temp solution to eable/disable custom parameter
		for i, cp in enumerate(Glyphs.font.customParameters):
				if cp.name == "glyphOrder":
					cp.setActive_(False)
					break
		Glyphs.font.customParameters[i].setActive_(False)

		self.colorLabels = {}
		labelUsed = self.font.userData["hugojourdan.RainbowFontView.labelUsed"]
		masterID = self.font.selectedFontMaster.id
		for glyph in self.font.glyphs:
			if labelUsed == "Glyph":
				color = glyph.color
			else:
				color = glyph.layers[masterID].color
			self.colorLabels.setdefault(color, [])
			self.colorLabels[color].append(glyph.name)

		self.colorLabels[13] = self.colorLabels.pop(None, [])
		self.colorLabels = OrderedDict(sorted(self.colorLabels.items()))

		self.code = ["#Color Layer Filter:"]
		for color, glyph in self.colorLabels.items():
			if str(color) in self.colorMeaning.keys():
				self.code.append(f"**{self.colorMeaning[str(color)]}**")
				self.code.extend(glyph)
			else:
				self.code.append(f"**No Color**")
				self.code.extend(glyph)

		# Update Layer Color Data in font.tempData
		self.font.tempData['saveColorLayers'] = self.colorLabels
		self.font.customParameters[i].setActive_(True)

		self.font.customParameters["glyphOrder"] = self.code

		return self.code, self.colorLabels

	@objc.python_method
	def getKeyFile(self):
		keyFile = None

		# Create info folder if missing
		infoFolder = f"{GSGlyphsInfo.applicationSupportPath()}/info"
		if not os.path.exists(infoFolder):
			os.makedirs(infoFolder)

		# Get colorNames.txt file next to Glyph file
		try:
			thisDirPath = os.path.dirname(self.windowController().document().font.filepath)
			localKeyFile = thisDirPath + '/colorNames.txt'
			if os.path.exists(localKeyFile):
				keyFile = localKeyFile
		except:
			keyFile = f"{GSGlyphsInfo.applicationSupportPath()}/info/colorNames.txt"

		if not os.path.exists(keyFile):	
			Message(f"If you want to customise Color Names,\n your settings file is here :\n\n ~/Library/Application Support/Glyphs 3/info/colorNames.txt\n\n", title='Settings file', OKButton=None)
			with open(keyFile, 'w', encoding='utf8') as f:
				config = "None=🫥 None\nred=🚨 Red\norange=🦊 Orange\nbrown=🪵 Brown\nyellow=🌼 Yellow\nlightGreen=🍀 Light green\ndarkGreen=🫑 Dark green\nlightBlue=💎 Light blue\ndarkBlue=🌀 Dark blue\npurple=🔮 Purple\nmagenta=🌺 Magenta\nlightGray=🏐 Light Gray\ncharcoal=🎱 Charcoal"
				f.write(config)
		else:
			pass
		return keyFile

	@objc.python_method
	def mapKeys(self, keyFile):
		colorKeys = {"red":'0',
					"orange":'1',
					"brown":'2',
					"yellow":'3',
					"lightGreen":'4',
					"darkGreen":'5',
					"lightBlue":'6',
					"darkBlue":'7',
					"purple":'8',
					"magenta":'9',
					"lightGray":'10',
					"charcoal":'11'}
		order = []
		colourLabels = {}
		if os.path.exists(keyFile):
			with codecs.open(keyFile, "r", "utf-8") as file:
				for line in file:
					if "None" in line: continue
					parts = line.strip().split('=')
					if len(parts) != 2: continue
					colour, label = parts
					colour = colour.strip()
					label = label.strip()
					if not colour: continue
					colourLabels[colorKeys.get(colour)] = label
					order.append(colorKeys.get(colour))
		return colourLabels, order

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

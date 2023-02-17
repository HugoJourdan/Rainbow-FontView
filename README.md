# Rainbow FontView

Rainbow Fontview is a Glyphs plugin to filter FontView based on Label Color of Selected Master.  
As default, it will use Layer Color, but if you want to use Glyph Color instead, run this command in the Macro Panel :  

```python 
Glyphs.font.userData["hugojourdan.RainbowFontView.labelUsed"] = "Glyph"
```

When installed, `Rainbox Fontview` will be added in `FILE` Menu. 

⚠️ It use `glyphOrder` custom parameters to work, so if you have already set one, it will be overridden.

![Preview](https://user-images.githubusercontent.com/76793951/219363693-e97569ae-7db0-4f54-b46a-b34c1b568b29.png)

## Demo

https://user-images.githubusercontent.com/76793951/219362964-fd45a0c0-5e3e-4b9f-a645-b1a015297a93.mp4


## How to custom Color Names

The plugin requires a `colorNames.txt` file stored in either `~/Library/Application Support/Glyphs 3/info` or the same directory as the current Glyphs source file. Preference is given to the latter allowing for the sharing of the labelkey.txt file with glyphs source files to retain labelling information between project contributors. 

The `colorNames.txt` file requires the formatting `colorName=meaning`, with each key on a newline and with no space surrounding the '='. The order of the key will follow the order specified in the text file. An example, with the defined colorNames is given below. 

```
None=🫥 None
red=🚨 Red
orange=🦊 Orange
brown=🪵 Brown
yellow=🌼 Yellow
lightGreen=🍀 Light green
darkGreen=🫑 Dark green
lightBlue=💎 Light blue
darkBlue=🌀 Dark blue
purple=🔮 Purple
magenta=🌺 Magenta
lightGray=🏐 Light Gray
charcoal=🎱 Charcoal
```



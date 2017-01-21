# SVG Import for Adobe XD
A Python 3 script to insert SVG files into Adobe XD Project Files.

# Motivation
The XD team at Adobe have done a fantastic job developing Adobe Experience Design for MacOS and now for Windows. However, there are some features that are missing from the Windows version of the application have been in the Mac version for quite some time. One of the biggest features missing is the ability to insert SVG images into Adobe XD Projects. This script seeks to fill in that gap by utilizing the file structure of .xd files to insert SVGs.

# Dependencies
This script requires [xmltodict](https://github.com/martinblech/xmltodict) to be installed on Python 3.

~~**NOTE: SVG must be optimized so that they contain only `<svg>` as the root element followed by any `<path>` elements that are part of the image. This can be done manually or using a tool such as [svgo](https://github.com/svg/svgo).**~~

> **Thanks to some help from [szh123](https://github.com/szh123), we no longer have to optimize the SVG before using it in the tool!**

# How To Use
1. Create a new XD file and place a shape (such as ellipse, rectangle, Pen tool) NOT ON AN ARTBOARD
2. Then open up a command-line in the place where the XD file and SVG are located
3. Run `python insertsvg.py path_to_svg path_to_xd` replacing `path_to_svg` with the relative path to the SVG file and `path_to_xd` to the relative path to the XD file.
4. If successful, it should print out `SVG Added` and `Temporary Files Deleted`

# Known Limitations
* Doesn't work when there is an artboard in the file
* No fills, effects, outline colors

Please create Issues if you find any other bugs.

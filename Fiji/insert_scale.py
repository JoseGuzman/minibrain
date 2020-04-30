"""
insert_scale.py

Jose Guzman, jguzman@guzman-lab.com
Created: Thu Apr 30 16:54:58 CEST 2020

This is an ImageJ-pluging writen in python that inserts a 2 mm scalebar
on the image selected.
To install the plugin sue Plugins->Install Pluging... in Fiji and 
select this file.
"""

from ij import IJ, ImagePlus
from ij import WindowManager
from ij.io import OpenDialog

op = OpenDialog("Select an image")

img = IJ.openImage(op.getPath())

mytitle = op.getFileName()[:-4] + '_2mm.tiff'
# Reduce size 50%
myimg = IJ.run(img, "Scale...", "x=0.5 y=0.5 width=1024 height=768 interpolation=Bilinear average create title=" + str(mytitle))
IJ.run(myimg, "Set Scale...", "distance=65 known=1 unit=mm")
IJ.run(myimg, "Scale Bar...", "width=2 height=6 font=20 color=White background=None location=[Lower Right]") # 2 mm

if __name__ in ['__builtin__', '__main__']:
	pass
	

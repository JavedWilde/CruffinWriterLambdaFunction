import Helpers


fontFile = f'Fonts/SVGFONT ({0}).svg' #change numbers for different fonts, 0 - 18
gcode = Helpers.GetGcode(text = 'Happy Birthday Dude dabs', fontFile = fontFile, xOffset = 0, yOffset = 0, max_bed_x = 60, max_bed_y = 20, move_speed = 300, cut_speed = 300, letterLimit = 25, arThres = 8)

# the generate svg file is upside down, i kept it that way since it was easier to just flip and get true 0 starting point on x and y, no random offsets, for viewing on web, just scale by -1 on the y
# svg file is saved as svg.svg

# font files are files converted from ttf to svg glyphs using an online tool, if we wanna add a font, just need to drag drop and click a button
# xOffset, yOffset is the final offset applied to the print, we will calculate this based on the size and shape of the chocolate plate
# max_bed_x, max_bed_y is for setting the print size, in the gcode it snaps to x scale first, then checks if y is going off the bed, then scales accordingly
# arThres, im using the aspect ratio (x:y) of the generated text to decide if it should split in two lines or stay at one
# rest are self explanatory, move speed shouldnt exceed over 300 for now, will do more tests to figure what is the most reliable print speed, for now 300 is safe 

with open("drawing.gcode", "w") as f:
        f.write(gcode)











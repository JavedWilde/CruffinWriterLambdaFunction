import Helpers

fontFile = f'Fonts/SVGFONT ({0}).svg' #change numbers for different fonts 0 - 18

gcode = Helpers.GetGcode(text = 'Happy Birthday Dude', fontFile = fontFile, xOffset = 0, yOffset = 0, max_bed_x = 60, max_bed_y = 20, move_speed = 300, cut_speed = 300, letterLimit = 25, arThres = 8)
with open("drawing.gcode", "w") as f:
        f.write(gcode)









